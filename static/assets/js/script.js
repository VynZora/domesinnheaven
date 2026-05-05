/* *********** TABLE OF CONTENTS ***************

 01 Open Sidebar JS
 02 Mobile Dropdown JS
 03 Sticky Header JS
 04 Data Background JS
 05 Blog Social JS
 06 Contact Info JS
 07 Fancybox Video Popup JS
 08 Hero Slider Active JS
 09 Camping Slider Active JS
 10 Completed Project Slider Active JS
 11 Testimonial Slider Active JS
 12 Blog Slider Active JS
 13 What We Do Slider Active JS
 14 Testimonial Slider Active JS
 15 Gallery Slider Active JS
 16 Service Slider Active JS
 17 Recent Course Slider Active JS
 18 Aos JS
 19 Counter JS
 20 Ajax Form JS

************ TABLE OF CONTENTS ************** */

(function ($) {

    'use strict';

    $(window).on('load', function () {
        $('#preloader').delay(350).fadeOut('slow');
        $('body').delay(350).css({ 'overflow': 'visible' });
    })

    /*--------------------------------------------------------------
    01 Open Sidebar JS
    --------------------------------------------------------------*/
    $('[data-toggle="sidebar"]').on('click', function (e) {
        e.preventDefault();
        $('body').toggleClass('overflow-hidden');
        $('.off-canvas-sidebar').toggleClass('active');
        $('.off-canvas-sidebar-body').toggleClass('active');
    });

    $('[data-close="sidebar"]').on('click', function (e) {
        e.preventDefault();
        $('body').removeClass('overflow-hidden');
        $('.off-canvas-sidebar').removeClass('active');
        $('.off-canvas-sidebar-body').removeClass('active');
    });

    $('[data-toggle="menubar"]').on('click', function (e) {
        e.preventDefault();
        $('body').toggleClass('overflow-hidden');
        $('.off-canvas-menubar').toggleClass('active');
        $('.off-canvas-menubar-body').toggleClass('active');
    });

    $('[data-close="menubar"]').on('click', function (e) {
        e.preventDefault();
        $('body').removeClass('overflow-hidden');
        $('.off-canvas-menubar').removeClass('active');
        $('.off-canvas-menubar-body').removeClass('active');
    });


    /*--------------------------------------------------------------
    02 Mobile Dropdown JS
    --------------------------------------------------------------*/
    $('.off-canvas-menu .has-dropdown > a').on('click', function (e) {
        e.preventDefault();
        $(this).parent().toggleClass('active');
        $(this).parent().children('.sub-menu').slideToggle();
        $(this).parent().siblings().children('.sub-menu').slideUp();
        $(this).parent().siblings().removeClass('active');
    });

    /*--------------------------------------------------------------
    03 Sticky Header JS
    --------------------------------------------------------------*/

    let win = $(window);
    let sticky_id = $(".header-area");
    win.on('scroll', function () {
        let scroll = win.scrollTop();
        if (scroll < 245) {
            sticky_id.removeClass("sticky-header");
        } else {
            sticky_id.addClass("sticky-header");
        }
    });

    /*--------------------------------------------------------------
    04 Data Background JS
    --------------------------------------------------------------*/
    $("[data-background]").each(function () {
        $(this).css("background-image", "url(" + $(this).attr("data-background") + ")")
    });

    $("[data-bg-color]").each(function () {
        $(this).css("background", $(this).attr("data-bg-color"))
    });


    /*--------------------------------------------------------------
    05 Blog Social JS
    --------------------------------------------------------------*/
    $('.total-shared').on('click', function (e) {
        e.preventDefault();
        $(this).parent().toggleClass('active');
    });

    document.querySelectorAll('.blog-card').forEach(function(card) {
        card.addEventListener('mouseleave', function () {
            const shared = this.querySelector('.social-share');
            if (shared) {
                shared.classList.remove('active');
            }
        });
    });

    /*--------------------------------------------------------------
    06 Contact Info JS
    --------------------------------------------------------------*/
    $('.contact-info').on('mouseenter', function () {
        $(this).addClass('active').siblings().removeClass('active');
    });

    /*--------------------------------------------------------------
    07 Fancybox Video Popup JS
    --------------------------------------------------------------*/
    if (jQuery("[data-fancybox]").length > 0) {
        Fancybox.bind('[data-fancybox]', {
            Html: {
                youtube: {
                    controls: 0,
                    rel: 0,
                    fs: 0
                }
            }
        });
    }


    /*--------------------------------------------------------------
    08 Hero Slider Active JS
    --------------------------------------------------------------*/
    function animateSwiperElements(selector, init) {
        let animated = function () {
            $(selector + ' [data-animation]').each(function () {
                let anim = $(this).data('animation');
                let delay = $(this).data('delay');
                let duration = $(this).data('duration');

                $(this).removeClass('anim' + anim)
                    .addClass(anim + ' animate__animated')
                    .css({
                        webkitAnimationDelay: delay,
                        animationDelay: delay,
                        webkitAnimationDuration: duration,
                        animationDuration: duration
                    })
                    .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function () {
                        $(this).removeClass(anim + ' animate__animated');
                    });
            });
        };

        // Initial animation
        animated();

        // Remove animation classes on slide change start
        init.on('slideChange', function () {
            $(selector + ' [data-animation]').removeClass('animate__animated');
        });

        // Animate on slide change complete
        init.on('slideChange', animated);
    }

    if (jQuery(".hero-slider-active-1").length > 0) {
        let sliderActive1 = '.hero-slider-active-1 .swiper';
        let sliderInit1 = new Swiper(sliderActive1, {
            slidesPerView: 1,
            slidesPerColumn: 1,
            paginationClickable: true,
            loop: true,
            effect: 'fade',
            fadeEffect: {crossFade: true},
            autoplay: {
                delay: 5000,
                waitForTransition: true,
                disableOnInteraction: false
            },
            pagination: {
                el: '.hero-slider-pagination-1',
                clickable: true,
            },
            navigation: {
                nextEl: '.hero-slider-button-next-1',
                prevEl: '.hero-slider-button-prev-1',
            },
            a11y: false
        });

        animateSwiperElements(sliderActive1, sliderInit1);
    }

    if (jQuery(".hero-slider-active-2").length > 0) {
        let sliderActive2 = '.hero-slider-active-2 .swiper';
        let sliderInit2 = new Swiper(sliderActive2, {
            slidesPerView: 1,
            slidesPerColumn: 1,
            paginationClickable: true,
            loop: true,
            effect: 'fade',
            fadeEffect: {crossFade: true},
            autoplay: {
                delay: 5000,
                waitForTransition: true,
                disableOnInteraction: false
            },
            pagination: {
                el: '.hero-slider-pagination-2',
                clickable: true,
            },
            navigation: {
                nextEl: '.hero-slider-button-next-2',
                prevEl: '.hero-slider-button-prev-2',
            },
            a11y: false
        });

        animateSwiperElements(sliderActive2, sliderInit2);
    }

    if (jQuery(".hero-slider-active-3").length > 0) {
        let sliderActive3 = '.hero-slider-active-3 .swiper';
        let sliderInit3 = new Swiper(sliderActive3, {
            slidesPerView: 1,
            slidesPerColumn: 1,
            paginationClickable: true,
            loop: true,
            effect: 'fade',
            fadeEffect: {crossFade: true},
            autoplay: {
                delay: 5000,
                waitForTransition: true,
                disableOnInteraction: false
            },
            pagination: {
                el: '.hero-slider-pagination-3',
                clickable: true,
                renderBullet: function (index, className) {
                    return '<span class="' + className + '">' + (index + 1) + "</span>";
                },
            },
            navigation: {
                nextEl: '.hero-slider-button-next-3',
                prevEl: '.hero-slider-button-prev-3',
            },
            a11y: false
        });

        animateSwiperElements(sliderActive3, sliderInit3);
    }


    /*--------------------------------------------------------------
    09 Camping Slider Active JS
    --------------------------------------------------------------*/
    if (jQuery(".camping-slider-active .swiper").length > 0) {
        let campingSlider = new Swiper('.camping-slider-active .swiper', {
            loop: true,
            spaceBetween: 30,
            slidesPerView: 1,
            slidesPerColumn: 1,
            paginationClickable: true,
            centeredSlides: true,

            autoplay: {
                delay: 3000,
            },

            pagination: {
                el: '.camping-pagination',
                clickable: true,
            },

            navigation: {
                nextEl: '.camping-button-next',
                prevEl: '.camping-button-prev',
            },

            a11y: false,

            breakpoints: {
                320: {
                    slidesPerView: 1,
                    centeredSlides: false,
                },
                768: {
                    slidesPerView: 2,
                    centeredSlides: false,
                },
                1024: {
                    slidesPerView: 3,
                    centeredSlides: true,
                },
                1200: {
                    slidesPerView: 3,
                    centeredSlides: true,
                },
            },
        })
    }

    if (jQuery(".dome-types-slider-active .swiper").length > 0) {
        let domeTypesSlider = new Swiper('.dome-types-slider-active .swiper', {
            loop: true,
            spaceBetween: 30,
            slidesPerView: 1,
            slidesPerColumn: 1,
            paginationClickable: true,
            centeredSlides: true,

            autoplay: {
                delay: 4000,
            },

            pagination: {
                el: '.dome-types-pagination',
                clickable: true,
            },

            navigation: {
                nextEl: '.dome-types-button-next',
                prevEl: '.dome-types-button-prev',
            },

            a11y: false,

            breakpoints: {
                320: {
                    slidesPerView: 1,
                    centeredSlides: false,
                },
                768: {
                    slidesPerView: 2,
                    centeredSlides: false,
                },
                1024: {
                    slidesPerView: 3,
                    centeredSlides: true,
                },
                1200: {
                    slidesPerView: 4,
                    centeredSlides: true,
                },
            },
        })
    }

    if (jQuery(".camping-slider-active-2 .swiper").length > 0) {
        let campingSlider2 = new Swiper('.camping-slider-active-2 .swiper', {
            loop: true,
            spaceBetween: 30,
            slidesPerView: 1,
            slidesPerColumn: 1,
            paginationClickable: true,
            centeredSlides: true,

            autoplay: {
                delay: 3000,
            },

            pagination: {
                el: '.camping-pagination-2',
                clickable: true,
            },

            navigation: {
                nextEl: '.camping-button-next-2',
                prevEl: '.camping-button-prev-2',
            },

            a11y: false,

            breakpoints: {
                320: {
                    slidesPerView: 1,
                },
                768: {
                    centeredSlides: false,
                    slidesPerView: 2,
                },
                1024: {
                    slidesPerView: 3,
                    centeredSlides: true,
                },
                1200: {
                    slidesPerView: 3,
                    centeredSlides: true,
                },
            },
        })
    }

    if (jQuery(".camping-slider-active-3 .swiper").length > 0) {
        let campingSlider2 = new Swiper('.camping-slider-active-3 .swiper', {
            loop: true,
            spaceBetween: 30,
            slidesPerView: 1,
            slidesPerColumn: 1,
            paginationClickable: true,

            autoplay: {
                delay: 3000,
            },

            pagination: {
                el: '.camping-pagination-3',
                clickable: true,
            },

            navigation: {
                nextEl: '.camping-button-next-3',
                prevEl: '.camping-button-prev-3',
            },

            a11y: false,

            breakpoints: {
                320: {
                    slidesPerView: 1,
                },
                768: {
                    slidesPerView: 2,
                },
                1024: {
                    slidesPerView: 3,
                },
                1200: {
                    slidesPerView: 3,
                },
            },
        })
    }


    /*--------------------------------------------------------------
    10 Completed Project Slider Active JS
    --------------------------------------------------------------*/
    if (jQuery(".completed-project-slider-active .swiper").length > 0) {
        let completedProjectSlider = new Swiper('.completed-project-slider-active .swiper', {
            loop: true,
            spaceBetween: 30,
            slidesPerView: 1,
            slidesPerColumn: 1,
            paginationClickable: true,
            centeredSlides: true,
            speed: 1000,

            autoplay: {
                delay: 3000,
            },

            pagination: {
                el: '.completed-project-pagination',
                clickable: true,
            },

            navigation: {
                nextEl: '.completed-project-button-next',
                prevEl: '.completed-project-button-prev',
            },

            a11y: false,

            breakpoints: {
                320: {
                    slidesPerView: 1.05,
                },
                768: {
                    slidesPerView: 1.5,
                },
                1024: {
                    slidesPerView: 1.5,
                },
                1200: {
                    slidesPerView: 2.5,
                },
            },
        })
    }

    if (jQuery(".completed-project-slider-active-2 .swiper").length > 0) {
        let completedProjectSlider2 = new Swiper('.completed-project-slider-active-2 .swiper', {
            loop: true,
            spaceBetween: 30,
            slidesPerView: 1,
            slidesPerColumn: 1,
            paginationClickable: true,
            centeredSlides: true,
            speed: 1000,

            autoplay: {
                delay: 3000,
            },

            pagination: {
                el: '.completed-project-pagination-2',
                clickable: true,
            },

            navigation: {
                nextEl: '.completed-project-button-next-2',
                prevEl: '.completed-project-button-prev-2',
            },

            a11y: false,

            breakpoints: {
                320: {
                    slidesPerView: 1.05,
                },
                768: {
                    slidesPerView: 1.5,
                },
                1024: {
                    slidesPerView: 1.5,
                },
                1200: {
                    slidesPerView: 2.5,
                },
            },
        })
    }


    /*--------------------------------------------------------------
    11 Testimonial Slider Active JS
    --------------------------------------------------------------*/
    if (jQuery(".testimonial-slider-active .swiper").length > 0) {
        let testimonialSlider = new Swiper('.testimonial-slider-active .swiper', {
            loop: true,
            spaceBetween: 30,
            slidesPerView: 1.3,
            slidesPerColumn: 1,
            paginationClickable: true,
            centeredSlides: true,

            autoplay: {
                delay: 3000,
            },

            pagination: {
                el: '.testimonial-pagination',
                clickable: true,
            },

            navigation: {
                nextEl: '.testimonial-button-next',
                prevEl: '.testimonial-button-prev',
            },

            a11y: false,

            effect: "cards",
            grabCursor: true,

            cardsEffect: {
                slideShadows: false, // Optional: make it flatter like your image
                perSlideOffset: 14,  // Slight horizontal separation
                perSlideRotate: 0    // No rotation
            },

            breakpoints: {
                320: {
                    slidesPerView: 1.07,
                    cardsEffect: {
                        perSlideOffset: 8,
                    },
                },
                768: {
                    slidesPerView: 1.3,
                },
                1024: {
                    slidesPerView: 1.3,
                },
                1200: {
                    slidesPerView: 1.3,
                },
            },
        })
    }

    /*--------------------------------------------------------------
   12 Blog Slider Active JS
   --------------------------------------------------------------*/
    if (jQuery(".blog-slider-active .swiper").length > 0) {
        let blogSlider = new Swiper('.blog-slider-active .swiper', {
            loop: true,
            spaceBetween: 30,
            slidesPerView: 2,
            slidesPerColumn: 1,
            paginationClickable: true,
            // autoplay: {
            //     delay: 3000,
            // },

            pagination: {
                el: '.blog-pagination',
                clickable: true,
            },

            navigation: {
                nextEl: '.blog-button-next',
                prevEl: '.blog-button-prev',
            },

            a11y: false,

            breakpoints: {
                320: {
                    slidesPerView: 1,
                },
                768: {
                    slidesPerView: 1,
                },
                1024: {
                    slidesPerView: 1,
                },
                1200: {
                    slidesPerView: 2,
                },
                1440: {
                    slidesPerView: 2.7,
                },
            },
        })
    }


    /*--------------------------------------------------------------
   14 Testimonial Slider Active JS
   --------------------------------------------------------------*/
    if (jQuery(".testimonial-slider-active-2 .swiper").length > 0) {
        let testimonialSlider = new Swiper('.testimonial-slider-active-2 .swiper', {
            loop: true,
            spaceBetween: 30,
            slidesPerView: 3,
            slidesPerColumn: 1,
            paginationClickable: true,
            autoplay: {
                delay: 3000,
            },

            pagination: {
                el: '.testimonial-pagination-2',
                clickable: true,
            },

            navigation: {
                nextEl: '.testimonial-button-next-2',
                prevEl: '.testimonial-button-prev-2',
            },

            a11y: false,

            breakpoints: {
                320: {
                    slidesPerView: 1,
                },
                768: {
                    slidesPerView: 2,
                },
                1024: {
                    slidesPerView: 2,
                },
                1200: {
                    slidesPerView: 3,
                },
            },
        })
    }

    /*--------------------------------------------------------------
    15 Gallery Slider Active JS
    --------------------------------------------------------------*/
    if (jQuery(".gallery-slider-active .swiper").length > 0) {
        let gallerySlider = new Swiper('.gallery-slider-active .swiper', {
            loop: true,
            spaceBetween: 30,
            slidesPerView: 1,
            slidesPerColumn: 1,
            paginationClickable: true,
            autoplay: {
                delay: 3000,
            },

            pagination: {
                el: '.gallery-pagination',
                clickable: true,
            },

            navigation: {
                nextEl: '.gallery-button-next',
                prevEl: '.gallery-button-prev',
            },

            a11y: false,
        })
    }

    /*--------------------------------------------------------------
   16 Service Slider Active JS
   --------------------------------------------------------------*/
    if (jQuery(".service-slider-active .swiper").length > 0) {
        let serviceSlider = new Swiper('.service-slider-active .swiper', {
            loop: true,
            spaceBetween: 30,
            slidesPerView: 3,
            slidesPerColumn: 1,
            paginationClickable: true,
            // autoplay: {
            //     delay: 3000,
            // },

            pagination: {
                el: '.service-pagination',
                clickable: true,
            },

            navigation: {
                nextEl: '.service-button-next',
                prevEl: '.service-button-prev',
            },

            a11y: false,

            breakpoints: {
                320: {
                    slidesPerView: 1,
                },
                768: {
                    slidesPerView: 2,
                },
                1024: {
                    slidesPerView: 2,
                },
                1200: {
                    slidesPerView: 3,
                },
            },
        })
    }

    /*--------------------------------------------------------------
   17 Recent Course Slider Active JS
   --------------------------------------------------------------*/
    if (jQuery(".recent-course-slider-active .swiper").length > 0) {
        let courseSlider = new Swiper('.recent-course-slider-active .swiper', {
            loop: true,
            spaceBetween: 30,
            slidesPerView: 1,
            slidesPerColumn: 1,
            paginationClickable: true,
            autoplay: {
                delay: 3000,
            },

            pagination: {
                el: '.recent-course-pagination',
                clickable: true,
            },

            navigation: {
                nextEl: '.recent-course-button-next',
                prevEl: '.recent-course-button-prev',
            },

            a11y: false,
        })
    }

    /*--------------------------------------------------------------
   18 Aos JS
   --------------------------------------------------------------*/
    AOS.init({
        // Global settings:
        disable: false, // accepts following values: 'phone', 'tablet', 'mobile', boolean, expression or function
        startEvent: 'DOMContentLoaded', // name of the event dispatched on the document, that AOS should initialize on
        initClassName: 'aos-init', // class applied after initialization
        animatedClassName: 'aos-animate', // class applied on animation
        useClassNames: false, // if true, will add content of `data-aos` as classes on scroll
        disableMutationObserver: false, // disables automatic mutations' detections (advanced)
        debounceDelay: 50, // the delay on debounce used while resizing window (advanced)
        throttleDelay: 99, // the delay on throttle used while scrolling the page (advanced)


        // Settings that can be overridden on per-element basis, by `data-aos-*` attributes:
        offset: 120, // offset (in px) from the original trigger point
        delay: 0, // values from 0 to 3000, with step 50ms
        duration: 400, // values from 0 to 3000, with step 50ms
        easing: 'ease', // default easing for AOS animations
        once: true, // whether animation should happen only once - while scrolling down
        mirror: false, // whether elements should animate out while scrolling past them
        anchorPlacement: 'top-bottom', // defines which position of the element regarding to window should trigger the animation
    });

    /*--------------------------------------------------------------
    19 counter
    --------------------------------------------------------------*/
    new PureCounter();

    /*--------------------------------------------------------------
    20 Ajax Form
    --------------------------------------------------------------*/
    $(function() {

        // Get the form.
        var form = $('#contact-form');
        if (!form.length) {
            return;
        }

        // Keep legacy AJAX behavior only for mail.php based templates.
        var actionUrl = $(form).attr('action') || '';
        if (actionUrl.indexOf('mail.php') === -1) {
            return;
        }

        // Get the messages div.
        var formMessages = $('.form-message');

        // Set up an event listener for the contact form.
        $(form).submit(function(e) {
            // Stop the browser from submitting the form.
            e.preventDefault();

            // Serialize the form data.
            var formData = $(form).serialize();

            // Submit the form using AJAX.
            $.ajax({
                type: 'POST',
                url: $(form).attr('action'),
                data: formData
            })
                .done(function(response) {
                    // Make sure that the formMessages div has the 'success' class.
                    $(formMessages).removeClass('error');
                    $(formMessages).addClass('success');

                    // Set the message text.
                    $(formMessages).text(response);

                    // Clear the form.
                    $('#contact-form input,#contact-form textarea').val('');
                })
                .fail(function(data) {
                    // Make sure that the formMessages div has the 'error' class.
                    $(formMessages).removeClass('success');
                    $(formMessages).addClass('error');

                    // Set the message text.
                    if (data.responseText !== '') {
                        $(formMessages).text(data.responseText);
                    } else {
                        $(formMessages).text('Oops! An error occured and your message could not be sent.');
                    }
                });
        });

    });

})(jQuery);
