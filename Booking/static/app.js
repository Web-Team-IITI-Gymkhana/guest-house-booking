document.addEventListener("DOMContentLoaded", function() {
    const faqs = document.querySelectorAll(".faq");

    faqs.forEach(faq => {
        faq.addEventListener("click", function() {
            faq.classList.toggle("active");
        });
    });
});
