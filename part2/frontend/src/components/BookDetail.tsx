import { useState, useEffect, useCallback } from 'react';
import { useParams, Link } from 'react-router-dom';
import { fetchBookById, BookDetail as BookDetailType } from '../api/library';
import BorrowForm from './BorrowForm';

/** Formats an ISO date string to "03 Nov 2024", or returns null. */
function formatDate(dateString: string | null): string | null {
  if (!dateString) return null;
  return new Date(dateString).toLocaleDateString('en-GB', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  });
}

/** Detail page for a single book — author info, borrow history, and borrow form. */
function BookDetail() {
  const { id } = useParams<{ id: string }>();

  const [selectedBook, setSelectedBook] = useState<BookDetailType | null>(null);
  const [error, setError] = useState<string | null>(null);

  /** Fetches the book and stores it in state. Wrapped in useCallback so BorrowForm gets a stable reference. */
  const loadBook = useCallback(async function () {
    try {
      const book = await fetchBookById(id!);
      setSelectedBook(book);
    } catch {
      setError('Could not load book details. Is the Flask server running?');
    }
  }, [id]);

  useEffect(function () {
    loadBook();
  }, [loadBook]);

  if (selectedBook === null && error === null) {
    return (
      <div className="page">
        <p className="state-loading">Loading book...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="page">
        <p className="state-error">{error}</p>
      </div>
    );
  }

  const book = selectedBook!;

  return (
    <div className="page">
      <Link to="/books" className="back-link">All Books</Link>

      <h1>{book.title}</h1>

      <p className="section-header">Book Details</p>
      <div className="detail-grid">
        <span className="detail-label">Author</span>
        <span className="detail-value">{book.author.name}</span>

        <span className="detail-label">Nationality</span>
        <span className="detail-value">{book.author.nationality}</span>

        <span className="detail-label">Genre</span>
        <span className="detail-value">{book.genre}</span>

        <span className="detail-label">Published</span>
        <span className="detail-value mono">{book.published_year}</span>

        <span className="detail-label">ISBN</span>
        <span className="detail-value mono">{book.isbn}</span>

        <span className="detail-label">Copies Available</span>
        <span className="detail-value mono">{book.copies_available}</span>
      </div>

      <p className="section-header">About the Author</p>
      <p>{book.author.bio}</p>

      <p className="section-header">Borrow History</p>

      {book.borrow_history.length === 0 ? (
        <p className="state-empty">This book has not been borrowed yet.</p>
      ) : (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Member</th>
                <th>Borrowed</th>
                <th>Returned</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {book.borrow_history.map(function (record) {
                return (
                  <tr key={record.borrow_id}>
                    <td>
                      <Link to={`/members/${record.member_id}`}>
                        {record.member_name}
                      </Link>
                    </td>
                    <td className="mono">{formatDate(record.borrow_date)}</td>
                    <td className="mono">
                      {record.return_date ? formatDate(record.return_date) : '—'}
                    </td>
                    <td>
                      {record.return_date ? (
                        <span className="badge badge-returned">Returned</span>
                      ) : (
                        <span className="badge badge-on-loan">On Loan</span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

      <p className="section-header">Borrow This Book</p>
      <BorrowForm bookId={id!} onSuccess={loadBook} />
    </div>
  );
}

export default BookDetail;
