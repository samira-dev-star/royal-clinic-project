
        document.addEventListener('DOMContentLoaded', function() {
            // Add animation to the buttons on hover
            const buttons = document.querySelectorAll('a');
            buttons.forEach(btn => {
                btn.addEventListener('mouseenter', function() {
                    this.classList.add('transform', 'scale-[1.03]');
                });
                btn.addEventListener('mouseleave', function() {
                    this.classList.remove('transform', 'scale-[1.03]');
                });
            });
        });
