const text = "✨SolumaStudios"; 
let typingIndex = 1;
let isDeleting = false;

function type() {
  let displayText = text.substring(0, typingIndex);
  document.title = displayText;

  let speed = 350;

  if (!isDeleting && typingIndex === text.length) {
    speed = 400; 
    isDeleting = true;
  } else if (isDeleting && typingIndex === 1) {
    isDeleting = false;
  }

  typingIndex = isDeleting ? typingIndex - 1 : typingIndex + 1;

  setTimeout(type, speed + 100);
}

type();
