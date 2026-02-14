// Main JavaScript file for Smart Life Reminder

console.log('Smart Life Reminder System Loaded');

// ==================== NOTIFICATION SETTINGS ====================

// Store already shown notifications to avoid duplicates
const shownNotifications = new Set();
const NOTIFICATION_CHECK_INTERVAL = 60000; // Check every 1 minute
const DAILY_CHECKIN_HOURS = 9; // 9 AM
const DAILY_CHECKIN_CHECK_INTERVAL = 5 * 60000; // Check every 5 minutes if daily checkin should show

// ==================== UTILITY FUNCTIONS ====================

function formatDate(dateStr) {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
    });
}

function daysUntil(dateStr) {
    const today = new Date();
    const target = new Date(dateStr);
    const time = target.getTime() - today.getTime();
    const days = Math.ceil(time / (1000 * 3600 * 24));
    return days;
}

// ==================== BROWSER NOTIFICATIONS ====================

function showBrowserNotification(title, options = {}) {
    // Show browser desktop notification
    if ('Notification' in window) {
        if (Notification.permission === 'granted') {
            const notification = new Notification(title, {
                icon: options.icon || '⏰',
                tag: options.tag || 'task-reminder', // Prevents duplicate notifications
                ...options
            });
            
            // Click handler
            if (options.onClick) {
                notification.onclick = options.onClick;
            }
        } else if (Notification.permission !== 'denied') {
            Notification.requestPermission().then(permission => {
                if (permission === 'granted') {
                    new Notification(title, options);
                }
            });
        }
    }
}

// Request notification permission on page load
function requestNotificationPermission() {
    if ('Notification' in window && Notification.permission === 'default') {
        Notification.requestPermission();
    }
}

// ==================== REMINDER SYSTEM ====================

async function checkForReminders() {
    // Check if any tasks need reminders and show notifications
    try {
        const response = await fetch('/api/reminders');
        const data = await response.json();
        
        if (data.success && data.reminders.length > 0) {
            data.reminders.forEach(reminder => {
                // Use task ID to prevent duplicate notifications
                if (!shownNotifications.has(`reminder-${reminder.id}`)) {
                    showBrowserNotification(reminder.message, {
                        tag: `reminder-${reminder.id}`,
                        body: `Task: ${reminder.title}`,
                        icon: '⏰',
                        onClick: () => {
                            window.location.href = '/dashboard';
                        }
                    });
                    shownNotifications.add(`reminder-${reminder.id}`);
                }
            });
        }
    } catch (error) {
        console.error('Error checking reminders:', error);
    }
}

// ==================== DAILY CHECK-IN ====================

let dailyCheckinShownToday = false;

function shouldShowDailyCheckin() {
    // Check if we should show daily checkin
    const now = new Date();
    const hour = now.getHours();
    
    // Show at specified hour (9 AM by default)
    return hour === DAILY_CHECKIN_HOURS && !dailyCheckinShownToday;
}

async function showDailyCheckinNotification() {
    // Show daily checkin popup
    try {
        const response = await fetch('/api/daily-checkin');
        const data = await response.json();
        
        if (data.success) {
            showBrowserNotification(data.message, {
                body: 'Take a moment to plan your day',
                tag: 'daily-checkin',
                requireInteraction: true, // User must interact
                onClick: () => {
                    // Open modal if available
                    const modal = document.getElementById('addTaskModal');
                    if (modal) {
                        modal.classList.remove('hidden');
                    }
                }
            });
            
            dailyCheckinShownToday = true;
        }
    } catch (error) {
        console.error('Error showing daily checkin:', error);
    }
}

// ==================== MODAL NOTIFICATION SYSTEM ====================

function showTaskReminder(reminder) {
    // Show in-app modal reminder
    const modal = document.createElement('div');
    modal.className = 'reminder-modal';
    modal.innerHTML = `
        <div class="reminder-content urgency-${reminder.urgency}">
            <span class="close-btn">&times;</span>
            <h3>${reminder.message}</h3>
            <p>${reminder.title}</p>
            <div class="reminder-actions">
                <button class="btn btn-primary" onclick="location.href='/dashboard'">View Task</button>
                <button class="btn btn-secondary" onclick="this.parentElement.parentElement.parentElement.remove()">Dismiss</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Close button
    modal.querySelector('.close-btn').addEventListener('click', () => {
        modal.remove();
    });
    
    // Auto-remove after 3 seconds if critical
    if (reminder.urgency === 'critical') {
        setTimeout(() => {
            if (modal.parentElement) {
                modal.remove();
            }
        }, 3000);
    }
}

// ==================== INITIALIZATION ====================

// Request notification permission when page loads
document.addEventListener('DOMContentLoaded', () => {
    requestNotificationPermission();
    
    // Check for reminders immediately
    checkForReminders();
    
    // Check for reminders every minute
    setInterval(checkForReminders, NOTIFICATION_CHECK_INTERVAL);
    
    // Check for daily checkin every 5 minutes
    setInterval(() => {
        if (shouldShowDailyCheckin()) {
            showDailyCheckinNotification();
        }
    }, DAILY_CHECKIN_CHECK_INTERVAL);
});

// ==================== SHOW NOTIFICATION ON DEMAND (FOR TESTING) ====================

window.testNotification = function() {
    showBrowserNotification('Test: This is a test notification!', {
        body: 'If you see this, notifications are working! ✅',
        icon: '✅'
    });
};

window.testDailyCheckin = function() {
    showDailyCheckinNotification();
};
