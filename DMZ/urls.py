from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from DMZ.views import view, patient, homeCare, ForgetPassword, Doctor, Daignostic, BookAppointment, adminPannel

# from django.conf import settings

#html file path here
urlpatterns = [
    # ----------------------------------------views.py------------------------------------------------------------
    path("", view.index, name="index"),
    path("contact_us/",view.contact_us, name="contact"),
    path("FAQ/",view.FAQ, name="FAQ"),
    path("About_us/",view.About, name="About_us"),
    path("Services/",view.Service, name="Service"),
    path("Department/",view.Department, name="Department"),
    path("Tele/",view.Tele, name="Tele"),
    path("Review/<int:doctor_id>",view.review, name="Review"),
    path("changePass/",view.password, name="password"),
    path("specialist/",view.specialist, name="specialist"),
    path("Login/",view.Login, name="login"),
    path("otp/",view.otp_fun, name="otp_fun"),
    path("resend_otp/",view.resend_otp, name="resend_otp"),
    path("Success/",view.success, name="appointment"),
    path("Logout/", view.Logout, name='logout'),
     
    # ----------------------------------------patient.py------------------------------------------------------------
    # path("Registration/",views.Registration, name="registration"),
    path("PatientSave/",patient.user.PatientSave, name="PatientSave"),
    path("Patient_Registration/",patient.user.patientRegistration, name="Patient_Registration"),
    path("Patient_home/<int:patient_id>",patient.user.patient_home, name="patient_home"),

    # ----------------------------------------ForgetPassword.py------------------------------------------------------------
    path("ForgetPassword/",ForgetPassword.ForgetPassword, name="forget"),
    path("ForgetByMobile/",ForgetPassword.ForgetByMobile, name="ForgetByMobile"),
    path("ForgetByQuestion/",ForgetPassword.ForgetByQuestion, name="ForgetByQuestion"),

    # ----------------------------------------Doctor.py------------------------------------------------------------
    path("doctor_home/<int:doctor_id>",Doctor.doctor_home, name="doctor_home"),
    path("doctor_profile/<int:doctor_id>/<str:doctor_category>",Doctor.doctor_profile, name="doctor_profile"),
    path("doctor_specilaity/<int:index>",Doctor.doctor_specilaity, name="doctor_specilaity"),
    path("doctors/",Doctor.doctors, name="doctors"),
    path("Doctor_Registration/",Doctor.doctorRegistration, name="Doctor_Registration"),

    # ----------------------------------------BookAppointment.py------------------------------------------------------------
    path("BookAppointment/<int:doctor_id>",BookAppointment.BookAppointment, name="appointment"),

    # ---------------------------------------------Daignostic.py-----------------------------------------------------------
    path("Diagnostic/",Daignostic.Diagnostic, name="Diagnostic"),
    path("ComboDiagnostic/",Daignostic.ComboDignostic, name="ComboDignostic"),
    path("ComboDiagnosticDetails/<int:id>",Daignostic.ComboDiagnosticDetails, name="ComboDiagnosticDetails"),
    path("DiagnosticDetails/<int:id>",Daignostic.DiagnosticDetails, name="DiagnosticDetails"),
    path("DignosticForm/",Daignostic.DignosticForm, name="DignosticForm"),
    # path("DignoCart/",views.DignoCart, name="DignoCart"),
    path("Digno-Add-To-Cart/<int:id>",Daignostic.DignoAddToCart, name="Digno_Add_To_Cart"),
    path("DignoCartItemDelete/<int:id>",Daignostic.DeleteCartItem, name="DeleteCartItem"),


    # ---------------------------------------------homeCare.py-----------------------------------------------------------
    # path("Medicine/",views.Medicine, name="Medicine"),
    path("HomeCare/",homeCare.HomeCare, name="HomeCare"),

    # ----------------------------------------adminPannel.py------------------------------------------------------------
    path("Admin_dash/",adminPannel.Admin_dashboard, name="Admin_dashboard"),
    path("Doctor_edit/<int:doctor_id>",adminPannel.admin_edit_doctor, name="doctor_edit"),
    path("Patient_edit/<int:patient_id>",adminPannel.admin_edit_Patient, name="patient_edit"),
    path("Admin_dash_doctor/",adminPannel.Admin_dashboard_doctor, name="Admin_dashboard"),
    path("Admin_dash_patient/",adminPannel.Admin_dashboard_patient, name="Admin_dashboard"),
    path("Admin_dash_patientDetails/",adminPannel.patient_details, name="patient_details"),
    path("Admin_dash_DoctorDetails/",adminPannel.doctor_details, name="doctor_details"),
    path("Admin_dash_doctorLogin/",adminPannel.Admin_dashboard_doctorLogin, name="dmin_dashboard"),
    path("Admin_dash_appointment/",adminPannel.admin_dashboard_appointmnet, name="admin_dashboard_appointmnet"),
    path("Admin_dash_test_appointment/",adminPannel.Admin_dash_test_appointment, name="Admin_dash_test_appointment"),
    path("Admin_dash_test/",adminPannel.Admin_dash_test, name="Admin_dash_test"),
    path("Admin_specialist/",adminPannel.Admin_specialist, name="Admin_specialist"),
    path("Admin_combo_test/",adminPannel.Admin_combo_test, name="Admin_combo_test"),
    path("Admin_dash_homerCare/",adminPannel.admin_dashboard_homeCare, name="Admin_dash_homerCare"),
    path("admin_dashboard_QNA/",adminPannel.admin_dashboard_QNA, name="admin_dashboard_QNA"),
    path("admin_dashboard_UpdateMedicine/<int:id>",adminPannel.UpdateMedicine, name="UpdateMedicine"),
    path("Admin_Update_test/<int:id>",adminPannel.Admin_Update_test, name="Admin_Update_test"),
    path("Admin_combo_Edit/<int:id>",adminPannel.Admin_combo_Edit, name="Admin_combo_Edit"),
    path("Admin_LabTest_Upload/",adminPannel.Admin_LabTest_Upload, name="Admin_LabTest_Upload"),
    path("admin_bill/",adminPannel.admin_bill, name="admin_bill"),
    path("deletePatient/<int:Id>", adminPannel.deletePt, name='delete'),
    path("deleteDoctor/<int:Id>", adminPannel.deleteDr, name='deleteDr'),
    path("deleteSingleTest/<int:id>", adminPannel.deleteSingleTest, name='deleteSingleTest'),
    path("deleteComboTest/<int:id>", adminPannel.deleteComboTest, name='deleteComboTest'),
    path("deleteAppointmentBill/<int:id>", adminPannel.deleteAppointmentBill, name='deleteAppointmentBill'),
    path("deleteMedicineBill/<str:id>", adminPannel.deleteMedicineBill, name='deleteMedicineBill'),
    path("deleteAppointment/<str:id>", adminPannel.deleteAppointment, name='deleteAppointment'),
    path("deleteHome", adminPannel.deleteHome, name='deleteHome'),
    path("admin_logout/", adminPannel.admin_logout, name='admin_logout'),
    
]