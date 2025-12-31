document.addEventListener('DOMContentLoaded', () => {
    const cursor = document.querySelector('.cursor');
    const follower = document.querySelector('.cursor-follower');
    
    let posX = 0, posY = 0;
    let mouseX = 0, mouseY = 0;
    
    // Only enable custom cursor if device has fine pointer (mouse)
    if (window.matchMedia("(pointer: fine)").matches) {
        
        document.addEventListener('mousemove', (e) => {
            mouseX = e.clientX;
            mouseY = e.clientY;
            
            // Immediate update for the small dot
            cursor.style.left = mouseX + 'px';
            cursor.style.top = mouseY + 'px';
        });
        
        // Smooth follow for the circle
        setInterval(() => {
            posX += (mouseX - posX) / 9;
            posY += (mouseY - posY) / 9;
            
            follower.style.left = posX + 'px';
            follower.style.top = posY + 'px';
        }, 10);
        
        // Add hover classes
        const links = document.querySelectorAll('a, .card');
        
        links.forEach(link => {
            link.addEventListener('mouseenter', () => {
                cursor.style.transform = 'translate(-50%, -50%) scale(0.5)';
                follower.style.transform = 'translate(-50%, -50%) scale(1.5)';
                follower.style.backgroundColor = 'rgba(255, 255, 255, 0.1)';
                follower.style.borderColor = 'transparent';
            });
            
            link.addEventListener('mouseleave', () => {
                cursor.style.transform = 'translate(-50%, -50%) scale(1)';
                follower.style.transform = 'translate(-50%, -50%) scale(1)';
                follower.style.backgroundColor = 'transparent';
                follower.style.borderColor = 'rgba(255, 255, 255, 0.5)';
            });
        });
    }
});