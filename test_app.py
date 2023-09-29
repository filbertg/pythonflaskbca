import unittest
from flask_testing import TestCase
from flask import url_for
from clinic import app, db, Patients, Appointments  # Import modul-modul yang diperlukan

# Kelas MyTest untuk melakukan testing pada aplikasi
class MyTest(TestCase):

    # Metode untuk membuat aplikasi dalam mode testing
    def create_app(self):
        app.config['TESTING'] = True  # Mengaktifkan mode testing
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinic.db'  # Menggunakan database in-memory untuk testing
        return app

    # Metode yang dijalankan sebelum setiap test
    def setUp(self):
        db.create_all()  # Membuat semua tabel dalam database

    # Metode yang dijalankan setelah setiap test
    def tearDown(self):
        db.session.remove()  # Menghapus sesi database
        db.drop_all()  # Menghapus semua tabel dalam database

    # Test untuk endpoint index '/'
    def test_index(self):
        response = self.client.get('/')  # Melakukan request GET ke '/'
        self.assert200(response)  # Memastikan response adalah 200 OK
        self.assert_template_used('index.html')  # Memastikan template yang digunakan adalah 'index.html'

    # Test untuk membuat pasien baru
    def test_create_patient(self):
        # Melakukan request POST ke '/input-patients' dengan data pasien baru
        response = self.client.post('/input-patients', json={
            'name': 'Filbert',
            'age': 19,
            'medical_history': 'Sakit perut'
        })
        self.assertStatus(response, 201)  # Memastikan response adalah 201 Created
        patient = Patients.query.first()  # Mengambil karyawan pertama dari database
        self.assertEqual(patient.name, 'Filbert')  # Memastikan nama pasien adalah 'Filbert'

    def test_create_appointment(self):
        # Melakukan request POST ke '/input-patients' dengan data pasien baru
        response = self.client.post('/input-patients', json={
            'name': 'Filbert',
            'age': 19,
            'medical_history': 'Sakit perut'
        })
        # Melakukan request POST ke '/input-patients' dengan data appointment baru
        response = self.client.post('/input-appointment', json={
            'patient_id': '1',
            'doctor_name': 'Surya',
            'date': '2023-09-29 10:30',
            'diagnosis': 'Sakit perut'
        })
        self.assertStatus(response, 201)  # Memastikan response adalah 201 Created
        appointment = Appointments.query.first()  # Mengambil karyawan pertama dari database
        self.assertEqual(appointment.doctor_name, 'Surya')  # Memastikan nama pasien adalah 'Surya'

    # Test untuk menghapus pasien
    def test_delete_patient(self):
        # Membuat objek pasien baru dan menyimpannya ke database
        patient = Patients(name='FF', age=12, medical_history='Berak berak')
        db.session.add(patient)
        db.session.commit()

        # Melakukan request DELETE ke '/patient/{patient_id}'
        response = self.client.delete(f'/patient/{patient.patient_id}')
        self.assert200(response)  # Memastikan response adalah 200 OK
        self.assertIsNone(Patients.query.get(patient.patient_id))  # Memastikan pasien dengan id tersebut sudah dihapus

    # Test untuk menghapus pasien
    def test_delete_appointment(self):
        # Membuat objek pasien baru dan menyimpannya ke database
        patient = Patients(name='FF', age=12, medical_history='Berak berak')
        db.session.add(patient)
        db.session.commit()
        appointment = Appointments(patient_id=patient.patient_id, doctor_name="Surya", date="2023-09-29 10:30", diagnosis="Sakit Perut")
        db.session.add(appointment)
        db.session.commit()

        # Melakukan request DELETE ke '/appointment/{appointment_id}'
        response = self.client.delete(f'/appointment/{appointment.appointment_id}')
        self.assert200(response)  # Memastikan response adalah 200 OK
        self.assertIsNone(Appointments.query.get(appointment.appointment_id))  # Memastikan appointment dengan id tersebut sudah dihapus

    # Test untuk mendapatkan semua pasien
    def test_get_all_patients(self):
        # Membuat dua objek pasien baru dan menyimpannya ke database
        pasien1 = Patients(name='Fausta', age=12, medical_history='amnesia')
        pasien2 = Patients(name='Fili', age=21, medical_history='hipertensi')
        db.session.add(pasien1)
        db.session.add(pasien2)
        db.session.commit()

        # Melakukan request GET ke '/display-patients'
        response = self.client.get('/display-patients')
        self.assert200(response)  # Memastikan response adalah 200 OK
        self.assert_template_used('displaypatients.html')  # Memastikan template yang digunakan adalah 'displaypatients.html'
        self.assertIn(b'Fausta', response.data)  # Memastikan 'Fausta' ada dalam response data
        self.assertIn(b'Fili', response.data)  # Memastikan 'Fili' ada dalam response data
    
    # Test untuk mendapatkan semua pasien
    def test_get_all_appppointments(self):
        # Membuat objek patient supaya bisa di refer sama objek appointment
        patient = Patients(name='Fausta', age=12, medical_history='amnesia')
        db.session.add(patient)
        db.session.commit()

        # Membuat dua objek karyawan baru dan menyimpannya ke database
        appointment1 = Appointments(patient_id=patient.patient_id, doctor_name="Surya", date="2023-09-29 10:30", diagnosis="Sakit Perut")
        appointment2 = Appointments(patient_id=patient.patient_id, doctor_name="Suryo", date="2023-09-29 10:30", diagnosis="Sakit Perut")
        db.session.add(appointment1)
        db.session.add(appointment2)
        db.session.commit()

        # Melakukan request GET ke '/display-appointments'
        response = self.client.get('/display-appointments')
        self.assert200(response)  # Memastikan response adalah 200 OK
        self.assert_template_used('displayappointments.html')  # Memastikan template yang digunakan adalah 'displayappointments.html'
        self.assertIn(b'Surya', response.data)  # Memastikan 'Surya' ada dalam response data
        self.assertIn(b'Suryo', response.data)  # Memastikan 'Suryo' ada dalam response data

if __name__ == '__main__':
    unittest.main()  # Menjalankan semua test
