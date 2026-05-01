# OMHA Mental Health Application - Testing Guide

## Quick Start
```bash
cd /workspaces/Our_Mental_Health_Assistance/omha-webapp
python omha.py
# Navigate to http://localhost:5000
```

---

## 1. Authentication & Authorization Testing

### 1.1 User Registration
- **Test**: Navigate to `/register`
- **Steps**:
  1. Enter username: `testuser1`
  2. Enter password: `testpass123`
  3. Click "Đăng ký"
- **Expected**: 
  - ✓ Success flash message appears
  - ✓ Redirects to login page
  - ✓ Can login with these credentials

### 1.2 Duplicate Username Prevention
- **Test**: Try registering with same username again
- **Expected**: 
  - ✓ Error flash message: "Username đã tồn tại!"
  - ✓ Not redirected, stays on register page

### 1.3 Login
- **Test**: Login with registered credentials
- **Steps**:
  1. Enter username: `testuser1`
  2. Enter password: `testpass123`
  3. Click "Đăng nhập"
- **Expected**:
  - ✓ Success - redirects to home page
  - ✓ Username appears in navbar: "Chào, testuser1!"

### 1.4 Failed Login
- **Test**: Login with wrong password
- **Expected**:
  - ✓ Error flash message: "Tài khoản hoặc mật khẩu không đúng!"
  - ✓ Stays on login page

### 1.5 Logout
- **Test**: Click logout button in navbar
- **Expected**:
  - ✓ Success flash message: "Đã đăng xuất thành công!"
  - ✓ Redirects to login
  - ✓ Username disappears from navbar

### 1.6 Login Required Protection
- **Test**: Try accessing `/diary` without login
- **Expected**:
  - ✓ Redirects to login page
  - ✓ Cannot access protected routes

---

## 2. Diary System Testing

### 2.1 Create Diary Entry
- **Test**: Create a new diary entry
- **Steps**:
  1. Click "Nhật ký" in navbar
  2. Select emotion: "Lo lắng 😨"
  3. Enter content: "Tôi đang cảm thấy căng thẳng vì kỳ thi sắp tới"
  4. Click "Lưu nhật ký"
- **Expected**:
  - ✓ Success flash: "Lưu nhật ký thành công!"
  - ✓ Entry appears in list with correct emotion emoji
  - ✓ Timestamp displayed correctly

### 2.2 Empty Entry Prevention
- **Test**: Try to save empty diary entry
- **Steps**:
  1. Click "Lưu nhật ký" without entering content
- **Expected**:
  - ✓ Warning flash: "Vui lòng nhập nội dung nhật ký!"
  - ✓ Entry not created

### 2.3 Newest-First Sorting
- **Test**: Create multiple diary entries
- **Expected**:
  - ✓ Newest entries appear at top
  - ✓ Oldest entries at bottom

### 2.4 Edit Diary Entry
- **Test**: Click "✏️ Sửa" on an entry
- **Steps**:
  1. Modify content
  2. Change emotion to "Biết ơn ❤️"
  3. Click "Cập nhật"
- **Expected**:
  - ✓ Success flash: "Cập nhật nhật ký thành công!"
  - ✓ Changes reflected in list
  - ✓ Timestamp unchanged

### 2.5 Edit Authorization Check
- **Test**: Logout, login as different user, try to access edit URL directly
- **Expected**:
  - ✓ Error flash: "You are not authorised to edit this entry."
  - ✓ Redirected to diary page

### 2.6 Delete Diary Entry
- **Test**: Click "🗑️ Xóa" on an entry
- **Expected**:
  - ✓ Success flash: "Đã xóa nhật ký thành công!"
  - ✓ Entry removed from list

---

## 3. Forum System Testing

### 3.1 View Forum
- **Test**: Click "Diễn đàn" in navbar
- **Expected**:
  - ✓ List of posts displayed
  - ✓ Shows title, preview, author, timestamp
  - ✓ "Đăng bài mới" button visible for logged-in users

### 3.2 Create Forum Post Without Image
- **Test**: Click "Đăng bài mới"
- **Steps**:
  1. Title: "Mẹo quản lý stress cho sinh viên"
  2. Content: "Hãy thực hành relaxation breathing..."
  3. Click "Đăng bài"
- **Expected**:
  - ✓ Post created successfully
  - ✓ Appears at top of forum list
  - ✓ Author name displayed correctly

### 3.3 Create Forum Post With Image
- **Test**: Create post with image
- **Steps**:
  1. Fill title and content
  2. Select image file (PNG/JPG/JPEG under 5MB)
  3. Click "Đăng bài"
- **Expected**:
  - ✓ Post created with image
  - ✓ Image displayed on post page
  - ✓ Image stored in `/uploads/` directory

### 3.4 Empty Post Prevention
- **Test**: Try to create post with empty content
- **Expected**:
  - ✓ Form validation error
  - ✓ Post not created

### 3.5 View Single Post
- **Test**: Click on a forum post
- **Expected**:
  - ✓ Full content displayed
  - ✓ Author and timestamp shown
  - ✓ Image displayed if present
  - ✓ Comments section visible

### 3.6 Add Comment
- **Test**: Add comment to a post
- **Steps**:
  1. Enter comment: "Cảm ơn bạn, mẹo này rất hữu ích!"
  2. Click "Post Comment"
- **Expected**:
  - ✓ Success flash: "Bình luận đã được đăng!"
  - ✓ Comment appears in list
  - ✓ Newest comments appear first

### 3.7 Empty Comment Prevention
- **Test**: Try to submit empty comment
- **Expected**:
  - ✓ Warning flash: "Vui lòng nhập nội dung bình luận!"
  - ✓ Comment not created

### 3.8 Comment Authorization
- **Test**: Try to comment without login (if logged out)
- **Expected**:
  - ✓ Error flash: "You must be logged in to comment."
  - ✓ Redirected to login

---

## 4. Articles & Videos Testing

### 4.1 View Content
- **Test**: Click "Bài viết" in navbar
- **Expected**:
  - ✓ Articles and videos displayed together
  - ✓ Sorted by date (newest first)
  - ✓ Shows title, preview, date

### 4.2 View Article Details
- **Test**: Click on an article
- **Expected**:
  - ✓ Full article content displayed
  - ✓ Author and category shown

### 4.3 Video Link
- **Test**: Click on a video
- **Expected**:
  - ✓ Opens video URL in new tab
  - ✓ Video platform loads (YouTube, etc.)

---

## 5. Chatbot Testing

### 5.1 Send Message
- **Test**: Open chatbot and send a message
- **Steps**:
  1. Click "Chatbot" in navbar
  2. Type: "Tôi cảm thấy lo lắng về kỳ thi"
  3. Click "Gửi" or press Enter
- **Expected**:
  - ✓ User message appears with blue badge
  - ✓ Typing indicator shows
  - ✓ Bot response appears after 2-5 seconds
  - ✓ Response is empathetic and Vietnamese
  - ✓ Messages persist after page reload

### 5.2 Enter Key Submission
- **Test**: Type message and press Enter
- **Expected**:
  - ✓ Message sends immediately
  - ✓ Works the same as clicking Gửi button

### 5.3 Empty Message Prevention
- **Test**: Try to send empty message
- **Expected**:
  - ✓ Warning flash: "Vui lòng nhập tin nhắn!"
  - ✓ Message not sent

### 5.4 Message History
- **Test**: Have a multi-turn conversation
- **Steps**:
  1. Send: "Tôi rất lo lắng"
  2. Send: "Đặc biệt là về tương lai"
  3. Send: "Bạn có thể giúp tôi không?"
- **Expected**:
  - ✓ All messages shown in chronological order
  - ✓ Bot can reference previous context
  - ✓ Conversation feels natural

### 5.5 Crisis Detection
- **Test**: Send high-risk message
- **Steps**:
  1. Type: "Tôi muốn tự tử"
- **Expected**:
  - ✓ Bot response changes to crisis response
  - ✓ Provides Vietnamese hotline numbers
  - ✓ Encourages seeking professional help
  - ✓ Shows empathy and concern

### 5.6 Save Message to Diary
- **Test**: Click "💾 Lưu vào nhật ký" on a bot message
- **Expected**:
  - ✓ Success flash: "Đã lưu tin nhắn vào nhật ký!"
  - ✓ Entry appears in diary with 🤖 emoji
  - ✓ Message content preserved

### 5.7 Quick Actions
- **Test**: Click quick action buttons
- **Steps**:
  1. Click "Mình đang căng thẳng"
  2. Click "Gửi"
- **Expected**:
  - ✓ Text fills input field
  - ✓ Message sends with that content

### 5.8 Clear Chat History
- **Test**: Click "🗑️ Xoá lịch sử"
- **Expected**:
  - ✓ Success flash: "Đã xoá lịch sử chat."
  - ✓ All messages disappear
  - ✓ Chat starts fresh

### 5.9 Conversation Persistence
- **Test**: Logout and login again
- **Expected**:
  - ✓ Chat history preserved for that user
  - ✓ Different users see different histories

---

## 6. Emotional Memory & Insight System Testing

### 6.1 Pattern Detection
- **Test**: Send multiple emotional messages
- **Steps**:
  1. Send: "Tôi rất lo lắng trước kỳ thi"
  2. Send: "Mỗi lần trước bài kiểm tra tôi đều sợ"
  3. Send: "Lo lắng làm tôi không thể ngủ"
- **Expected**:
  - ✓ Bot references past anxiety patterns
  - ✓ Personalizes responses
  - ✓ Shows understanding of recurring themes

### 6.2 Emotional Context Injection
- **Test**: Have long conversation
- **Expected**:
  - ✓ Bot mentions: "Tôi nhớ bạn từng nói về..."
  - ✓ References specific emotional patterns
  - ✓ Responses become more personalized

### 6.3 Insight Storage
- **Test**: Check database for emotional insights
- **Command**:
  ```bash
  sqlite3 instance/site.db "SELECT * FROM emotional_insight;"
  ```
- **Expected**:
  - ✓ Insights stored with emotion_type, description, trigger
  - ✓ Frequency increased on repeated patterns
  - ✓ last_observed timestamp updated

---

## 7. Error Handling & User Feedback Testing

### 7.1 Database Error Handling
- **Test**: Perform operations that might fail
- **Expected**:
  - ✓ Errors caught and logged
  - ✓ User sees friendly error message
  - ✓ No white screen of death

### 7.2 Flash Messages
- **Test**: Perform any action (create, edit, delete)
- **Expected**:
  - ✓ Green success message for successful actions
  - ✓ Red danger message for errors
  - ✓ Yellow warning for input validation
  - ✓ Blue info for informational messages
  - ✓ Dismissible with X button

### 7.3 Network Error Handling (Chatbot API)
- **Test**: Stop internet connection temporarily
- **Steps**:
  1. Send chatbot message
  2. Disable network
  3. Re-enable network
- **Expected**:
  - ✓ Graceful error handling
  - ✓ User sees: "😢 Chatbot tạm thời bận..."
  - ✓ No app crash

### 7.4 Input Validation Across Forms
- **Test**: Submit forms with invalid data
- **Expected**:
  - ✓ Empty fields rejected
  - ✓ Helpful validation messages shown
  - ✓ Data not corrupted

---

## 8. User Experience Improvements Testing

### 8.1 Responsive Design
- **Test**: View app on different screen sizes
- **Expected**:
  - ✓ Desktop (1920px): Full layout
  - ✓ Tablet (768px): Collapsed navbar
  - ✓ Mobile (375px): Single column layout
  - ✓ All buttons clickable on mobile

### 8.2 Navigation
- **Test**: Navigate between all pages
- **Expected**:
  - ✓ Navbar links work correctly
  - ✓ Breadcrumbs or back buttons available
  - ✓ No broken links

### 8.3 Accessibility Features
- **Test**: Click theme toggle in navbar
- **Steps**:
  1. Click 🌙 button
  2. Refresh page
  3. Click ☀️ button
- **Expected**:
  - ✓ Dark mode/light mode toggles
  - ✓ Preference persists
  - ✓ Text remained readable

### 8.4 Text Size Adjustment
- **Test**: Click A+ and A- buttons
- **Expected**:
  - ✓ Text increases with A+
  - ✓ Text decreases with A-
  - ✓ Preference saved in localStorage

### 8.5 High Contrast Mode
- **Test**: Click ⚡ button
- **Expected**:
  - ✓ Contrast increases for accessibility
  - ✓ Preference persists

---

## 9. Security Testing

### 9.1 Password Hashing
- **Test**: Check database for raw passwords
- **Command**:
  ```bash
  sqlite3 instance/site.db "SELECT username, password_hash FROM user LIMIT 1;"
  ```
- **Expected**:
  - ✓ Password is hashed (bcrypt)
  - ✓ Not readable plaintext

### 9.2 User Data Isolation
- **Test**: Login as user1, view diary
- **Steps**:
  1. Note diary entries
  2. Logout, login as user2
  3. Check diary
- **Expected**:
  - ✓ User2 sees only their entries
  - ✓ Cannot access user1's data

### 9.3 CSRF Protection
- **Test**: Create post with form
- **Expected**:
  - ✓ Form includes CSRF token
  - ✓ POST requests validated

---

## 10. Performance Testing

### 10.1 Large Message History
- **Test**: Send 50+ messages in chatbot
- **Expected**:
  - ✓ Chat remains responsive
  - ✓ Only last 40 messages included in API context
  - ✓ No memory leaks

### 10.2 Large Diary Entries
- **Test**: Create diary entry with 5000+ characters
- **Expected**:
  - ✓ Saves correctly
  - ✓ Displays without performance issues

### 10.3 Multiple New Users
- **Test**: Register 5+ users simultaneously
- **Expected**:
  - ✓ All registrations succeed
  - ✓ No database conflicts

---

## 11. Cross-Browser Testing

### 11.1 Chrome/Chromium
- **Steps**: Run app, test all features
- **Expected**: ✓ All working

### 11.2 Firefox
- **Steps**: Run app, test all features
- **Expected**: ✓ All working

### 11.3 Safari
- **Steps**: Run app, test all features
- **Expected**: ✓ All working

---

## 12. API Integration Testing

### 12.1 Gemini API Connection
- **Test**: Send chatbot message and check logs
- **Expected**:
  - ✓ API call logged
  - ✓ No timeout errors
  - ✓ Response within 5 seconds

### 12.2 API Fallback
- **Test**: Temporarily change API key to invalid
- **Expected**:
  - ✓ Bot tries fallback model
  - ✓ Shows error message if all fail
  - ✓ No app crash

---

## Quick Test Checklist

```
Authentication:
☐ Register new user
☐ Duplicate username rejected
☐ Login works
☐ Logout works
☐ Protected routes require login

Diary:
☐ Create entry
☐ Edit entry
☐ Delete entry
☐ Empty entry rejected
☐ Sort newest first

Forum:
☐ Create post without image
☐ Create post with image
☐ Add comment
☐ Empty post rejected
☐ Empty comment rejected

Chatbot:
☐ Send message
☐ Receive response
☐ Enter key works
☐ Crisis detection works
☐ Save to diary works
☐ Clear history works

Articles:
☐ View articles/videos
☐ Sorted by date
☐ Can click to view

Error Handling:
☐ Flash messages appear
☐ Validation prevents empty input
☐ Database errors handled
☐ API failures graceful

UX:
☐ Responsive on mobile
☐ Dark/light mode works
☐ Accessibility features work
☐ Navigation works
```

---

## Database Schema Check

```bash
sqlite3 instance/site.db ".schema"
```

Expected tables:
- `user` ✓
- `diary_entry` ✓
- `forum_post` ✓
- `comment` ✓
- `article` ✓
- `video` ✓
- `chat_message` ✓
- `emotional_insight` ✓

---

## Logs & Debugging

### View Flask Logs
```bash
python omha.py 2>&1 | grep -E "ERROR|WARNING|INFO"
```

### Check Database
```bash
sqlite3 instance/site.db
.tables
.schema
SELECT COUNT(*) FROM user;
SELECT COUNT(*) FROM chat_message;
SELECT COUNT(*) FROM emotional_insight;
```

### View Uploads
```bash
ls -la uploads/
```

---

## Known Limitations & Notes

1. **Eventlet Deprecation**: App uses eventlet which is deprecated. Consider migrating to Gunicorn + gevent
2. **API Key**: Gemini API key stored in .env (should use Vault in production)
3. **Database**: SQLite for development; use PostgreSQL for production
4. **Real-time Features**: SocketIO configured but video call not fully implemented
5. **Image Storage**: Files stored locally; use S3/Cloud Storage in production

---

## Performance Benchmarks

Target metrics:
- Page load: < 500ms
- Chatbot response: < 5s
- Form submission: < 200ms
- Database query: < 100ms

---

## Reporting Issues

If you find bugs during testing, check:
1. Flask console for error messages
2. Browser console for JavaScript errors
3. Database integrity with `.schema` command
4. File uploads in `uploads/` directory

