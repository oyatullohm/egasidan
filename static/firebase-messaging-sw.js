// firebase-messaging-sw.js

importScripts('https://www.gstatic.com/firebasejs/8.10.0/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/8.10.0/firebase-messaging.js');

firebase.initializeApp({
  apiKey: "AIzaSyBTWh23G8dOx_dE6rXFjH-6OCArLwIPcDg",
  authDomain: "egasidan-35edc.firebaseapp.com",
  projectId: "egasidan-35edc",
  storageBucket: "egasidan-35edc.firebasestorage.app",
  messagingSenderId: "1044507351309",
  appId: "1:1044507351309:web:2bd1282ff17114fc9f3844"
});

const messaging = firebase.messaging();

// 🔔 Orqa fonda (background) xabar kelsa
messaging.setBackgroundMessageHandler(function(payload) {
  console.log('📩 Background xabar:', payload);
  const title = payload.notification.title;
  const options = {
    body: payload.notification.body,
    // icon: '/static/logo.png'
  };
  return self.registration.showNotification(title, options);
});
