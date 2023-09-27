# Import Library
from flask import Flask, jsonify, request, render_template
from flask import redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger, swag_from
from datetime import datetime
import os

# Mendefinisikan app
app = Flask(__name__)

# Konfigurasi database
app.config['SQLALCHEMY_ECH0'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:jhmEAccHJ0EdjNdDCtuJ@containers-us-west-108.railway.app:7821/railway'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SWAGGER'] = {
    'title': 'Sistem Informasi Manajemen Pasien untuk Klinik API',
    'uiversion': 3,
    'header': [],
    'specs': [
        {
            'endpoint': 'apispec_1',
            'route': '/apispec_1.json',
            'rule_filter': lambda rule: True,
            'model_filter': lambda rule: True,
        }
    ],
    'static_url_path': '/flasgger_static',
    'swagger_ui': True,
    'specs_route': '/apidocs/'
}

swagger = Swagger(app)

db = SQLAlchemy(app)

# Model Data Karyawan
class Patients(db.Model):
    patient_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    age = db.Column(db.Integer, nullable = False)
    medical_history = db.Column(db.String(255))

class Appointments(db.Model):
    appointment_id = db.Column(db.Integer, primary_key = True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id'),nullable = False)
    doctor_name = db.Column(db.String(100), nullable = False)
    date = db.Column(db.DateTime)
    diagnosis = db.Column(db.String(255))

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/display-patients', methods = ['GET'])
@swag_from('C:/Users/user/Documents/Training/Python/finalproject/project/swagger_docs/get_all_data_patients.yaml')
def get_all_patients():
    patients_list = []
    try:
        # Mengambil semua data patient dari database
        all_patients = Patients.query.all()

        # Membuat daftar dari data patient untuk dikirimkan ke template
        for patient in all_patients:
            patient_data = {
                'patient_id': patient.patient_id,
                'name': patient.name,
                'age': patient.age,
                'medical_history': patient.medical_history
            }
            patients_list.append(patient_data)
    except Exception as e :
        # Mengembalikan pesan jika terjadi kesalahan
        return render_template('error.html', pesan="Terjadi kesalahan saat mengambil data pasien : {}".format(str(e))), 500
    finally:
        if patients_list:
            return render_template('displaypatients.html', patients_list = patients_list)
        else:
            # Mengembalikan pesan kesalahan jika tidak ada data pasien
            return render_template('error.html', pesan = "Tidak ada data pasien yang dapat ditampilkan"), 404

@app.route('/display-appointments', methods = ['GET'])
@swag_from('C:/Users/user/Documents/Training/Python/finalproject/project/swagger_docs/get_all_data_appointments.yaml')
def get_all_appointments():
    appointments_list = []
    try:
        # Mengambil semua data patient dari database
        all_appointments = Appointments.query.all()

        # Membuat daftar dari data patient untuk dikirimkan ke template
        for appointment in all_appointments:
            appointment_data = {
                'appointment_id': appointment.appointment_id,
                'patient_id': appointment.patient_id,
                'doctor_name': appointment.doctor_name,
                'date': appointment.date,
                'diagnosis': appointment.diagnosis
            }
            appointments_list.append(appointment_data)
    except Exception as e :
        # Mengembalikan pesan jika terjadi kesalahan
        return render_template('error.html', pesan="Terjadi kesalahan saat mengambil data janji temu : {}".format(str(e))), 500
    finally:
        if appointments_list:
            return render_template('displayappointments.html', appointments_list = appointments_list)
        else:
            # Mengembalikan pesan kesalahan jika tidak ada data pasien
            return render_template('error.html', pesan = "Tidak ada data janji temu yang dapat ditampilkan"), 404

@app.route('/create-patients', methods = ['GET', 'POST'])
@swag_from('C:/Users/user/Documents/Training/Python/finalproject/project/swagger_docs/create_data_patients.yaml')
def create_patients():
    if request.method == "POST":
        # Mendapatkan data dari form
        name = request.form.get('name')
        age = request.form.get('age')
        medical_history = request.form.get('medical_history')

        if not name or not age:
            return render_template('createpatient.html', error = "Semua field wajib diisi!")

        # Membuat objek karyawan
        new_patient = Patients (
            name = name,
            age = age,
            medical_history = medical_history
        )

        # Proses simpan data
        db.session.add(new_patient)
        db.session.commit()

        # Mengarahkan ke halaman konfirmasi
        return render_template('confirmation.html')
        
    return render_template('createpatient.html')

@app.route('/createappointment', methods = ['GET', 'POST'])
def createappointment():
    if request.method == "POST":
        name = request.form.get('name')
        patients_list = Patients.query.filter(Patients.name.like(f"%{name}")).all()
        return render_template('createappointment.html', patients_list = patients_list)
    return render_template('createappointment.html')

@app.route('/create-appointment', methods = ['POST'])
@swag_from('C:/Users/user/Documents/Training/Python/finalproject/project/swagger_docs/create_data_appointments.yaml')
def create_appointments():
    patient_id = request.form.get('patient_id')
    doctor_name = request.form.get('doctor_name')
    date = request.form.get('date')
    date_value = datetime.strptime(date, '%Y-%m-%dT%H:%M')
    diagnosis = request.form.get('diagnosis')

    if not patient_id or not doctor_name or not date:
        return render_template('createappointment.html', error = "Semua field wajib diisi!")
        
    new_appointment = Appointments (
        patient_id = patient_id,
        doctor_name = doctor_name,
        date = date_value,
        diagnosis = diagnosis
    )

    # Proses simpan data
    db.session.add(new_appointment)
    db.session.commit()

    # Mengarahkan ke halaman konfirmasi
    return render_template('confirmation.html')    

@app.route('/updatepatient', methods = ['GET', 'POST'])
def updatepatients():
    if request.method == "POST":
        name = request.form.get('name')
        patients_list = Patients.query.filter(Patients.name.like(f"%{name}")).all()
        return render_template('updatepatient.html', patients_list = patients_list)
    return render_template('updatepatient.html')

@app.route('/update-patient', methods = ['POST'])
@swag_from('C:/Users/user/Documents/Training/Python/finalproject/project/swagger_docs/update_data_patients.yaml')
def update_patients():
    try:
        # Ambil data dari form
        patient_id = request.form.get('patient_id')
        name = request.form.get('name')
        age = request.form.get('age')
        medical_history = request.form.get('medical_history')

        # Temukan karyawan berdasarkan id_karyawan
        patient = Patients.query.get(patient_id)

        if not patient:
            return jsonify({'message': 'Data pasien tidak ditemukan'}), 404
        
        # Update data karyawan
        patient.name = name
        patient.age = age
        patient.medical_history = medical_history

        # Simpan perubahan ke database
        db.session.commit()

        return redirect(url_for('get_all_patients'))
    except Exception as e:
        return jsonify({'message': f'Terjadi kesalahan: {str(e)}'}), 500

@app.route('/updateappointment', methods = ['GET', 'POST'])
def updateappointment():
    if request.method == "POST":
        name = request.form.get('name')
        patients_list = Patients.query.filter(Patients.name.like(f"%{name}")).all()
        appointments_list = []
        for patients in patients_list:
            all_appointment = Appointments.query.filter(Appointments.patient_id.like(patients.patient_id)).all()
            for appointment in all_appointment:
                appointments_list.append(appointment)

        if appointments_list:
            return render_template('updateappointment.html', appointments_list = appointments_list)
    return render_template('updateappointment.html')
        

@app.route('/update-appointment', methods = ['POST'])
@swag_from('C:/Users/user/Documents/Training/Python/finalproject/project/swagger_docs/update_data_appointments.yaml')
def update_appointments():
    try:
        # Ambil data dari form
        appointment_id = request.form.get('appointment_id')
        doctor_name = request.form.get('doctor_name')
        date = request.form.get('date')
        date_value = datetime.strptime(date, '%Y-%m-%dT%H:%M')
        print(date)
        print(type(date))
        diagnosis = request.form.get('diagnosis')

        # Temukan karyawan berdasarkan id_karyawan
        appointment = Appointments.query.get(appointment_id)

        if not appointment:
            return jsonify({'message': 'Data pasien tidak ditemukan'}), 404
        
        # Update data karyawan
        appointment.doctor_name = doctor_name
        appointment.date = date_value
        appointment.diagnosis = diagnosis

        # Simpan perubahan ke database
        db.session.commit()

        return redirect(url_for('get_all_appointments'))
    except Exception as e:
        return jsonify({'message': f'Terjadi kesalahan: {str(e)}'}), 500

@app.route('/deletepatient', methods = ['GET', 'POST'])
def deletepatient():
    patients_list = []
    try:
        if request.method == 'POST':
            search_name = request.form['name'].lower()
            all_patients = Patients.query.all()

            patients_list = [patient for patient in all_patients if search_name in patient.name.lower()]
    except Exception as e:
        error_message = f"Terjadi kesalahan: {e}"
        print(error_message)
        return render_template('error.html', pesan = error_message), 500
    finally:
        return render_template('deletepatient.html', patients_list = patients_list)

@app.route('/patient/<int:patient_id>', methods = ['DELETE'])
@swag_from('C:/Users/user/Documents/Training/Python/finalproject/project/swagger_docs/delete_data_patients.yaml')
def delete_patients(patient_id):
    try:
        # Cari pasien berdasarkan patient_id
        patient_to_delete = Patients.query.filter_by(patient_id=patient_id).first()
        # Jika pasien ditemukan, hapus dari database
        if patient_to_delete:
            db.session.delete(patient_to_delete)
            db.session.commit()
            return jsonify({'message': f'Data karyawan dengan ID {patient_id} berhasil dihapus'}), 200
        else:
            return jsonify({'message': f'Data karyawan dengan ID {patient_id} tidak ditemukan'}), 404
    except Exception as e:
        return jsonify({'message': f'Terjadi kesalahan: {e}'}), 500

@app.route('/deleteappointment', methods = ['GET', 'POST'])
def deleteappointment():
    appointments_list = []
    try:
        if request.method == "POST":
            name = request.form.get('name')
            patients_list = Patients.query.filter(Patients.name.like(f"%{name}")).all()
            
            for patients in patients_list:
                all_appointment = Appointments.query.filter(Appointments.patient_id.like(patients.patient_id)).all()
                for appointment in all_appointment:
                    appointments_list.append(appointment)

    except Exception as e:
        error_message = f"Terjadi kesalahan: {e}"
        print(error_message)
        return render_template('error.html', pesan = error_message), 500
    finally:
        return render_template('deleteappointment.html', appointments_list = appointments_list) 

@app.route('/appointment/<int:appointment_id>', methods = ['DELETE'])
@swag_from('C:/Users/user/Documents/Training/Python/finalproject/project/swagger_docs/delete_data_appointments.yaml')
def delete_appointments(appointment_id):
    try:
        # Cari appointment berdasarkan appointment_id
        appointment_to_delete = Appointments.query.filter_by(appointment_id=appointment_id).first()
        # Jika appointment ditemukan, hapus dari database
        if appointment_to_delete:
            db.session.delete(appointment_to_delete)
            db.session.commit()
            return jsonify({'message': f'Data karyawan dengan ID {appointment_id} berhasil dihapus'}), 200
        else:
            return jsonify({'message': f'Data karyawan dengan ID {appointment_id} tidak ditemukan'}), 404
    except Exception as e:
        return jsonify({'message': f'Terjadi kesalahan: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True)