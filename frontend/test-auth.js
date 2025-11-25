// Simple test script to verify authentication flow
fetch('/api/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    username: 'ranger1',
    password: 'password'
  })
})
.then(response => response.json())
.then(data => {
  console.log('Login response:', data);
  
  if (data.token) {
    // Test getting user info
    return fetch('/api/auth/user', {
      headers: {
        'Authorization': `Bearer ${data.token}`
      }
    });
  }
})
.then(response => response.json())
.then(userData => {
  console.log('User info response:', userData);
})
.catch(error => {
  console.error('Error:', error);
});