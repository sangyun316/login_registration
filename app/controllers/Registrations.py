from system.core.controller import *

class Registrations(Controller):
    def __init__(self, action):
        super(Registrations, self).__init__(action)
        self.load_model('Registration')
        self.db = self._app.db
   
    def index(self):
        return self.load_view('index.html')

    def register(self):
        user_info = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': request.form['password'],
            'confirm_pw': request.form['confirm_pw']
        }
        register_status = self.models['Registration'].register_user(user_info)
        if register_status['status'] == False:
            for message in register_status['errors']:
                flash(message)
            return redirect('/')
        else:
            session['first_name'] = request.form['first_name']
            return redirect('/success')

    def login(self):
        user_info = {
            'email': request.form['email'],
            'password': request.form['password']
        }
        user = self.models['Registration'].login_validation(user_info)
        if user:
            session['first_name'] = user[0]['first_name']
            return redirect('/success')
        else:
            flash('Email or password is incorrect. Please log-in again!')
            return redirect('/')

    def success(self):
        return self.load_view('index2.html')

    def logout(self):
        session.clear()
        return redirect('/')
    	