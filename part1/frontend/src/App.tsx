import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Nav from './components/Nav';
import BookList from './components/BookList';
import BookDetail from './components/BookDetail';
import MemberList from './components/MemberList';
import MemberDetail from './components/MemberDetail';

/** Root component — declares all client-side routes. */
function App() {
  return (
    <BrowserRouter>
      <Nav />
      <Routes>
        <Route path="/" element={<Navigate to="/books" replace />} />
        <Route path="/books" element={<BookList />} />
        <Route path="/books/:id" element={<BookDetail />} />
        <Route path="/members" element={<MemberList />} />
        <Route path="/members/:id" element={<MemberDetail />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
