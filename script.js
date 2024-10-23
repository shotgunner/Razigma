const tg = window.Telegram.WebApp;

// Main Button
function showMainButton() {
    tg.MainButton.setText("submit");
    tg.MainButton.show();
    tg.MainButton.onClick(foo);
}

function hideMainButton() {
    tg.MainButton.hide();
}

// Back Button
function showBackButton() {
    tg.BackButton.show();
}

function hideBackButton() {
    tg.BackButton.hide();
}

// Haptic Feedback
function impactOccurred() {
    tg.HapticFeedback.impactOccurred("medium");
}

function notificationOccurred() {
    tg.HapticFeedback.notificationOccurred("success");
}

function selectionChanged() {
    tg.HapticFeedback.selectionChanged();
}

// Closing WebApp
function closeWebApp() {
    tg.close();
}

// Ready event
tg.onEvent('viewportChanged', () => {
    console.log('Viewport changed');
});

// Expand the webapp to maximum available height
tg.expand();

// Show main button when the page opens
window.addEventListener('load', showMainButton);

// Function to handle submit button click
function foo() {
    const inputData = document.querySelector('input[type="text"]').value;
    const username = tg.initDataUnsafe?.user?.username || 'Unknown';
    const userId = tg.initDataUnsafe?.user?.id || 'Unknown';
    alert(`telegram username: ${username}\nuser id: ${userId}\ninput data: ${inputData}`);
}