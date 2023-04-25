const express = require('express');
const crypto = require('crypto');
const path = require('path');

const API_KEY = 'QSad0m5NQkq2XoeT8s8osw';
const API_SECRET = 'nouE624RlF7aXznFSIKvN6Yjb0x6244z';

const app = express();
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

app.post('/api/signature', (req, res) => {
  const meetingNumber = req.body.meetingNumber;
  const role = req.body.role || 0;
  const timestamp = new Date().getTime() - 30000;
  const msg = Buffer.from(API_KEY + meetingNumber + timestamp + role).toString('base64');
  const hash = crypto.createHmac('sha256', API_SECRET).update(msg).digest('base64');
  const signature = Buffer.from(`${API_KEY}.${meetingNumber}.${timestamp}.${role}.${hash}`).toString('base64');
  res.json({ signature });
});

app.listen(3000, () => console.log('Server listening on port 3000!'));
