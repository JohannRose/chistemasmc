from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from flask_compress import Compress
from forms import LoginForm, PlayerForm, PaymentForm, ExpenseForm
import database as db
import static_cache

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'minecraft-payment-tracker-johann-2025-secret-key-production'

# Enable HTTP Compression for faster responses
Compress(app)

# Optimize Flask settings
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # Cache static files for 1 year
app.config['TEMPLATES_AUTO_RELOAD'] = False  # Disable in production
app.config['JSON_SORT_KEYS'] = False  # Faster JSON responses

# NO POOL INITIALIZATION - Direct connections only

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, user_dict):
        self.id = user_dict['id']
        self.username = user_dict['username']

@login_manager.user_loader
def load_user(user_id):
    user_data = db.execute_one("SELECT * FROM users WHERE id = %s", (int(user_id),))
    return User(user_data) if user_data else None


# ============================================================================
# PUBLIC ROUTES
# ============================================================================

@app.route('/')
def index():
    """Public page - STATIC CACHE (actualiza cada 5 minutos)"""
    data = static_cache.get_index_data()
    return render_template('index.html',
                         player_data=data['player_data'],
                         payments=data['payments'],
                         expenses=data['expenses'],
                         total_collected=data['total_collected'],
                         total_expenses=data['total_expenses'],
                         overall_balance=data['overall_balance'],
                         expense_per_player=data['expense_per_player'])


# ============================================================================
# ADMIN AUTHENTICATION
# ============================================================================

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    """Admin login"""
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user_data = db.get_user_by_username(form.username.data)
        if user_data and db.verify_password(user_data, form.password.data):
            user = User(user_data)
            login_user(user)
            flash('Inicio de sesión exitoso!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('admin_dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    
    return render_template('admin/login.html', form=form)


@app.route('/admin/logout')
@login_required
def logout():
    """Logout"""
    logout_user()
    flash('Has cerrado sesión exitosamente', 'info')
    return redirect(url_for('index'))


# ============================================================================
# ADMIN DASHBOARD
# ============================================================================

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    """Dashboard - OPTIMIZED with cached queries"""
    stats = db.get_statistics()
    recent_payments = db.get_recent_payments(5)
    recent_expenses = db.get_recent_expenses(5)
    
    return render_template('admin/dashboard.html',
                         total_players=stats['total_players'],
                         total_collected=float(stats['total_collected']),
                         total_expenses=float(stats['total_expenses']),
                         overall_balance=float(stats['overall_balance']),
                         recent_payments=recent_payments,
                         recent_expenses=recent_expenses)


# ============================================================================
# PLAYERS
# ============================================================================

@app.route('/admin/players')
@login_required
def admin_players():
    players = db.get_all_players()
    return render_template('admin/players.html', players=players)


@app.route('/admin/players/add', methods=['GET', 'POST'])
@login_required
def add_player():
    form = PlayerForm()
    if form.validate_on_submit():
        db.create_player(form.name.data, form.minecraft_username.data)
        static_cache.force_refresh_index()
        flash(f'Jugador {form.name.data} agregado exitosamente!', 'success')
        return redirect(url_for('admin_players'))
    return render_template('admin/add_player.html', form=form)


@app.route('/admin/players/edit/<int:player_id>', methods=['GET', 'POST'])
@login_required
def edit_player(player_id):
    player = db.get_player_by_id(player_id)
    if not player:
        flash('Jugador no encontrado', 'danger')
        return redirect(url_for('admin_players'))
    
    form = PlayerForm(data=player)
    if form.validate_on_submit():
        db.update_player(player_id, form.name.data, form.minecraft_username.data)
        static_cache.force_refresh_index()
        flash(f'Jugador {form.name.data} actualizado exitosamente!', 'success')
        return redirect(url_for('admin_players'))
    
    return render_template('admin/edit_player.html', form=form, player=player)


@app.route('/admin/players/delete/<int:player_id>', methods=['POST'])
@login_required
def delete_player(player_id):
    player = db.get_player_by_id(player_id)
    if player:
        db.delete_player(player_id)
        static_cache.force_refresh_index()
        flash(f'Jugador {player["name"]} eliminado exitosamente', 'success')
    return redirect(url_for('admin_players'))


# ============================================================================
# PAYMENTS
# ============================================================================

@app.route('/admin/payments')
@login_required
def admin_payments():
    payments = db.get_all_payments()
    return render_template('admin/payments.html', payments=payments)


@app.route('/admin/payments/add', methods=['GET', 'POST'])
@login_required
def add_payment():
    form = PaymentForm()
    players = db.get_all_players()
    form.player_id.choices = [(p['id'], f"{p['name']} ({p['minecraft_username']})") for p in players]
    
    if form.validate_on_submit():
        db.create_payment(form.player_id.data, form.amount.data, form.date.data, form.description.data)
        static_cache.force_refresh_index()
        flash(f'Pago de S/{form.amount.data} registrado exitosamente!', 'success')
        return redirect(url_for('admin_payments'))
    
    return render_template('admin/add_payment.html', form=form)


@app.route('/admin/payments/edit/<int:payment_id>', methods=['GET', 'POST'])
@login_required
def edit_payment(payment_id):
    payment = db.get_payment_by_id(payment_id)
    if not payment:
        flash('Pago no encontrado', 'danger')
        return redirect(url_for('admin_payments'))
    
    form = PaymentForm(data=payment)
    players = db.get_all_players()
    form.player_id.choices = [(p['id'], f"{p['name']} ({p['minecraft_username']})") for p in players]
    
    if form.validate_on_submit():
        db.update_payment(payment_id, form.player_id.data, form.amount.data, form.date.data, form.description.data)
        static_cache.force_refresh_index()
        flash(f'Pago de S/{form.amount.data} actualizado exitosamente!', 'success')
        return redirect(url_for('admin_payments'))
    
    return render_template('admin/edit_payment.html', form=form, payment=payment)


@app.route('/admin/payments/delete/<int:payment_id>', methods=['POST'])
@login_required
def delete_payment(payment_id):
    db.delete_payment(payment_id)
    static_cache.force_refresh_index()
    flash('Pago eliminado exitosamente', 'success')
    return redirect(url_for('admin_payments'))


# ============================================================================
# EXPENSES
# ============================================================================

@app.route('/admin/expenses')
@login_required
def admin_expenses():
    expenses = db.get_all_expenses()
    return render_template('admin/expenses.html', expenses=expenses)


@app.route('/admin/expenses/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    form = ExpenseForm()
    if form.validate_on_submit():
        db.create_expense(form.amount.data, form.date.data, form.description.data)
        static_cache.force_refresh_index()
        flash(f'Gasto de S/{form.amount.data} registrado exitosamente!', 'success')
        return redirect(url_for('admin_expenses'))
    
    return render_template('admin/add_expense.html', form=form)


@app.route('/admin/expenses/edit/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    expense = db.get_expense_by_id(expense_id)
    if not expense:
        flash('Gasto no encontrado', 'danger')
        return redirect(url_for('admin_expenses'))
    
    form = ExpenseForm(data=expense)
    if form.validate_on_submit():
        db.update_expense(expense_id, form.amount.data, form.date.data, form.description.data)
        static_cache.force_refresh_index()
        flash(f'Gasto de S/{form.amount.data} actualizado exitosamente!', 'success')
        return redirect(url_for('admin_expenses'))
    
    return render_template('admin/edit_expense.html', form=form, expense=expense)


@app.route('/admin/expenses/delete/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense(expense_id):
    db.delete_expense(expense_id)
    static_cache.force_refresh_index()
    flash('Gasto eliminado exitosamente', 'success')
    return redirect(url_for('admin_expenses'))


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
