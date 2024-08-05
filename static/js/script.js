particlesJS("particles-js", {
    "particles": {
        "number": { "value": 80, "density": { "enable": true, "value_area": 800 } },
        "color": { "value": "#3366cc" },
        "shape": { "type": "circle" },
        "opacity": { "value": 0.5, "random": false },
        "size": { "value": 3, "random": true },
        "line_linked": { "enable": true, "distance": 150, "color": "#3366cc", "opacity": 0.4, "width": 1 },
        "move": { "enable": true, "speed": 6 }
    },
    "interactivity": {
        "detect_on": "canvas",
        "events": {
            "onhover": { "enable": true, "mode": "repulse" },
            "onclick": { "enable": true, "mode": "push" },
            "resize": true
        }
    },
    "retina_detect": true
});

$(document).ready(function() {
    let currentStep = 1;
    let selectedSpecialty = '';
    let selectedDoctor = '';
    let selectedDate = '';
    let selectedTime = '';

    function goToNextStep() {
        if (currentStep < 5) {
            $(`#step${currentStep}`).removeClass('active');
            currentStep++;
            $(`#step${currentStep}`).addClass('active');
            updateProgressIndicator();
        }
    }

    function goToPreviousStep() {
        if (currentStep > 1) {
            $(`#step${currentStep}`).removeClass('active');
            currentStep--;
            $(`#step${currentStep}`).addClass('active');
            updateProgressIndicator();
        }
    }

    function updateProgressIndicator() {
        $('.progress-step').removeClass('active');
        for (let i = 1; i <= currentStep; i++) {
            $(`.progress-step[data-step=${i}]`).addClass('active');
        }
    }

    $('.specialty-card').on('click', function() {
        $('.specialty-card').removeClass('selected');
        $(this).addClass('selected');
        selectedSpecialty = $(this).data('specialty');
        $('#nextToStep2').prop('disabled', false);
    });

    $('#nextToStep2').on('click', function() {
        goToNextStep();

        const doctors = [
            { id: 1, name: 'دکتر علی محمدی', specialty: 'cardiology' },
            { id: 2, name: 'دکتر نادر سلطانی', specialty: 'cardiology' },
            { id: 3, name: 'دکتر لیلا هاشمی', specialty: 'cardiology' },
            { id: 4, name: 'دکتر امیر صالحی', specialty: 'cardiology' },
            { id: 5, name: 'دکتر سارا قاسمی', specialty: 'cardiology' },
            { id: 6, name: 'دکتر مریم احمدی', specialty: 'neurology' },
            { id: 7, name: 'دکتر سیاوش معین', specialty: 'neurology' },
            { id: 8, name: 'دکتر مهسا رستمی', specialty: 'neurology' },
            { id: 9, name: 'دکتر فرزاد کیانی', specialty: 'neurology' },
            { id: 10, name: 'دکتر گلناز احمدی', specialty: 'neurology' },
            { id: 11, name: 'دکتر حسن رضایی', specialty: 'orthopedics' },
            { id: 12, name: 'دکتر سمیرا نیکو', specialty: 'orthopedics' },
            { id: 13, name: 'دکتر محمد تقی پور', specialty: 'orthopedics' },
            { id: 14, name: 'دکتر یاسر احمدی', specialty: 'orthopedics' },
            { id: 15, name: 'دکتر نرگس عباس زاده', specialty: 'orthopedics' },
            { id: 16, name: 'دکتر آزاده کاظمی', specialty: 'dermatology' },
            { id: 17, name: 'دکتر سامان دهقان', specialty: 'dermatology' },
            { id: 18, name: 'دکتر آناهیتا مهدوی', specialty: 'dermatology' },
            { id: 19, name: 'دکتر میثم مرادی', specialty: 'dermatology' },
            { id: 20, name: 'دکتر کیانا جعفری', specialty: 'dermatology' },
            { id: 21, name: 'دکتر سروش حیدری', specialty: 'ophthalmology' },
            { id: 22, name: 'دکتر رعنا سبزی', specialty: 'ophthalmology' },
            { id: 23, name: 'دکتر امیرحسین ملاحی', specialty: 'ophthalmology' },
            { id: 24, name: 'دکتر مهتاب مهدی پور', specialty: 'ophthalmology' },
            { id: 25, name: 'دکتر علی اکبر معینی', specialty: 'ophthalmology' },
            { id: 26, name: 'دکتر حسین دینی', specialty: 'dentistry' },
            { id: 27, name: 'دکتر ندا قدیمی', specialty: 'dentistry' },
            { id: 28, name: 'دکتر پژمان نوروزی', specialty: 'dentistry' },
            { id: 29, name: 'دکتر مونا رضایی', specialty: 'dentistry' },
            { id: 30, name: 'دکتر فرشاد میرکاظمی', specialty: 'dentistry' }
        ];

        const filteredDoctors = doctors.filter(doc => doc.specialty === selectedSpecialty);
        $('#doctorList').empty();
        filteredDoctors.forEach(doc => {
            $('#doctorList').append(`
                <div class="col-md-4 mb-3">
                    <div class="card doctor-card" data-doctor-id="${doc.id}">
                        <div class="card-body text-center">
                            <h5 class="card-title">${doc.name}</h5>
                        </div>
                    </div>
                </div>
            `);
        });
    });

    $(document).on('click', '.doctor-card', function() {
        $('.doctor-card').removeClass('selected');
        $(this).addClass('selected');
        selectedDoctor = $(this).data('doctor-id');
        $('#nextToStep3').prop('disabled', false);
    });

    $('#nextToStep3').on('click', function() {
        goToNextStep();
        initializePersianDatepicker();
    });

    $('#backToStep1').on('click', function() {
        goToPreviousStep();
    });

    function initializePersianDatepicker() {
        const today = new Date();
        $("#persianDatepicker").pDatepicker({
            inline: true,
            format: 'YYYY/MM/DD',
            minDate: today,
            autoClose: false,
            onSelect: function(unix) {
                selectedDate = new Date(unix).toLocaleDateString('fa-IR');
                updateTimeSlots();
            }
        });
    }

    function updateTimeSlots() {
        $.ajax({
            url: '/check-availability',
            type: 'GET',
            data: {
                doctor_id: selectedDoctor,
                date: selectedDate
            },
            success: function(response) {
                const bookedTimes = response.bookedTimes;
                renderTimeSlots(bookedTimes);
            },
            error: function(xhr, status, error) {
                console.error('Error checking availability:', error);
                alert('خطا در بررسی زمان‌های در دسترس. لطفاً دوباره تلاش کنید.');
            }
        });
    }

    function renderTimeSlots(bookedTimes) {
        const timeSlots = [
            '08:00', '08:30',
            '09:00', '09:30',
            '10:00', '10:30',
            '11:00', '11:30',
            '12:00', '12:30',
            '13:00', '13:30',
            '14:00', '14:30',
            '15:00', '15:30',
            '16:00', '16:30',
            '17:00', '17:30',
            '18:00', '18:30',
            '19:00', '19:30'];

        const now = new Date();
        const selectedDateTime = new Date(selectedDate);
        const isToday = selectedDateTime.toDateString() === now.toDateString();

        $('#timeSlots').empty();
        timeSlots.forEach(time => {
            const [hours, minutes] = time.split(':').map(Number);
            const slotTime = new Date(selectedDateTime.getTime());
            slotTime.setHours(hours, minutes, 0, 0);
            
            const isPast = isToday && slotTime < now;
            const isBooked = bookedTimes.includes(time);

            const buttonClass = isPast || isBooked ? 'btn-danger' : 'btn-outline-primary';
            const disabled = isPast || isBooked ? 'disabled' : '';

            $('#timeSlots').append(`
                <div class="col">
                    <button type="button" class="btn ${buttonClass} time-slot-btn" ${disabled} data-time="${time}">${time}</button>
                </div>
            `);
        });
    }

    $(document).on('click', '.time-slot-btn:not(:disabled)', function() {
        $('.time-slot-btn').removeClass('active');
        $(this).addClass('active');
        selectedTime = $(this).data('time');
        $('#nextToStep4').prop('disabled', false);
    });

    $('#nextToStep4').on('click', function() {
        goToNextStep();
    });

    $('#backToStep2').on('click', function() {
        goToPreviousStep();
    });

    $('#nextToStep5').on('click', function() {
        const fullName = $('#fullName').val();
        const phoneNumber = $('#phoneNumber').val();
        const email = $('#email').val();
        const nationalId = $('#nationalId').val();
        const gender = $('input[name="gender"]:checked').val();
        const insuranceType = $('#insuranceType').val();
        const medicalHistory = $('#medicalHistory').val();

        if (fullName && phoneNumber && nationalId && gender && insuranceType) {
            $('#summarySpecialty').text(selectedSpecialty);
            $('#summaryDoctor').text(selectedDoctor);
            $('#summaryDateTime').text(`${selectedDate} - ${selectedTime}`);
            $('#summaryPersonalInfo').html(`
                نام: ${fullName}<br>
                شماره تماس: ${phoneNumber}<br>
                ایمیل: ${email}<br>
                کد ملی: ${nationalId}<br>
                جنسیت: ${gender}<br>
                نوع بیمه: ${insuranceType}<br>
                سابقه پزشکی: ${medicalHistory}
            `);
            goToNextStep();
        } else {
            alert('لطفاً تمامی فیلدهای مورد نیاز را پر کنید.');
        }
    });

    $('#backToStep3').on('click', function() {
        goToPreviousStep();
    });

    $('#backToStep4').on('click', function() {
        goToPreviousStep();
    });

    $('#submitAppointment').on('click', function(e) {
        e.preventDefault();

        const appointmentData = {
            specialty: selectedSpecialty,
            doctor_id: selectedDoctor,
            appointment_date: selectedDate,
            appointment_time: selectedTime,
            patient_name: $('#fullName').val(),
            phone_number: $('#phoneNumber').val(),
            email: $('#email').val(),
            national_id: $('#nationalId').val(),
            gender: $('input[name="gender"]:checked').val(),
            insurance_type: $('#insuranceType').val(),
            medical_history: $('#medicalHistory').val()
        };

        $.ajax({
            url: '/submit-appointment',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(appointmentData),
            success: function(response) {
                $('#successModal').modal('show');
                setTimeout(function() {
                    $('#successModal').modal('hide');
                    window.location.href = '/';
                }, 3000);
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
                console.error('Status:', status);
                console.error('Response:', xhr.responseText);
                alert('خطا در ثبت نوبت. لطفاً دوباره تلاش کنید. جزئیات خطا: ' + 'خطا از سمت vercel است زیرا از sqlite پشتیبانی نمیکند');
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', () => {
  const teamMembers = document.querySelectorAll('.team-member');

  teamMembers.forEach(member => {
    member.addEventListener('mouseenter', () => {
      member.style.transform = 'scale(1.05) translateY(-15px)';
    });

    member.addEventListener('mouseleave', () => {
      member.style.transform = 'scale(1) translateY(0)';
    });
  });

  // Parallax effect for the wave
  window.addEventListener('scroll', () => {
    const wave = document.querySelector('.footer-wave');
    const scrollPosition = window.pageYOffset;
    wave.style.transform = `translateY(${scrollPosition * 0.1}px) rotate(180deg)`;
  });
});