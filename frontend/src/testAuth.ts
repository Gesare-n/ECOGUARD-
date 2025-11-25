// Test authentication service
import authService from './services/authService';

// Test login
console.log('Testing authentication service...');

// Test getCurrentUser method
authService.getCurrentUser().then(user => {
  console.log('Current user:', user);
}).catch(error => {
  console.error('Error getting current user:', error);
});

// Test login
authService.login('ranger1', 'password').then(success => {
  console.log('Login success:', success);
  if (success) {
    console.log('Auth state after login:', authService.getState());
  }
}).catch(error => {
  console.error('Error during login:', error);
});