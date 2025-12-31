const contentEl = document.getElementById('content');
const clickSound = new Audio('https://www.soundjay.com/mechanical/sounds/typewriter-key-1.mp3'); 
// Note: External audio might be blocked or slow. Ideally we'd synthesize simple clicks.

// The text to "reveal" as the user types. 
// A mix of philosophy and code.
const sourceText = `
"The code is the canvas, the screen is the gallery."

function createArt() {
    const soul = new Soul();
    const reality = new Reality();
    
    while (soul.isAlive()) {
        try {
            const inspiration = reality.observe();
            soul.express(inspiration);
        } catch (existential_crisis) {
            soul.reflect();
            // Sometimes, the error is the art.
        }
    }
}

// In the silence of the digital void,
// we find the echo of our own thoughts.
// 01001000 01100101 01101100 01101100 01101111

To define is to limit.
To code is to create worlds.
Each keystroke a decision.
Each function a destiny.

Welcome to the flow state.
Where time dissolves into syntax.
And logic blooms into beauty.
`;

let currentIndex = 0;

document.addEventListener('keydown', (e) => {
    // Ignore modifier keys
    if (e.key.length > 1 && e.key !== 'Enter' && e.key !== 'Backspace') return;
    
    // Play sound (simulated simple click if file fails)
    // For simplicity in this demo, we skip actual audio file dependency to avoid CORS/404 issues
    // and just focus on the visual typing.
    
    if (e.key === 'Backspace') {
        if (currentIndex > 0) {
            currentIndex--;
            contentEl.innerText = sourceText.substring(0, currentIndex);
        }
        return;
    }

    // "Type" the next character from source regardless of what key was pressed
    if (currentIndex < sourceText.length) {
        currentIndex++;
        contentEl.innerText = sourceText.substring(0, currentIndex);
        
        // Auto-scroll
        window.scrollTo(0, document.body.scrollHeight);
    }
});

// Mobile touch support
document.addEventListener('touchstart', () => {
   // Trigger a keypress logic
   const e = { key: 'a' }; // Mock key
   document.dispatchEvent(new KeyboardEvent('keydown', e));
});