import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { fetchAllBooks, searchBooks, Book } from '../api/library';

/** The set of genre options shown in the filter dropdown. */
const GENRES = [
  'Contemporary Fiction',
  'Historical Fiction',
  'Literary Fiction',
  'Magical Realism',
  'Speculative Fiction',
  'Thriller',
];

/** Searchable, filterable table of every book. Loads via GET /books on mount; searches via GET /books/search. */
function BookList() {
  const [bookList, setBookList] = useState<Book[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [query, setQuery] = useState<string>('');
  const [selectedGenre, setSelectedGenre] = useState<string>('');
  const [isSearching, setIsSearching] = useState<boolean>(false);

  useEffect(function () {
    async function loadBooks() {
      try {
        const books = await fetchAllBooks();
        setBookList(books);
      } catch {
        setError('Could not load books. Is the Flask server running?');
      }
    }

    loadBooks();
  }, []);

  async function handleSearch(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsSearching(true);
    setError(null);

    try {
      const books = await searchBooks(query.trim(), selectedGenre);
      setBookList(books);
    } catch {
      setError('Search failed. Is the Flask server running?');
    } finally {
      setIsSearching(false);
    }
  }

  async function handleClear() {
    setQuery('');
    setSelectedGenre('');
    setError(null);

    try {
      const books = await fetchAllBooks();
      setBookList(books);
    } catch {
      setError('Could not reload books. Is the Flask server running?');
    }
  }

  if (bookList === null && error === null) {
    return (
      <div className="page">
        <p className="state-loading">Loading books...</p>
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

  const isFiltered = query.trim() !== '' || selectedGenre !== '';

  return (
    <div className="page">
      <h1>Book Catalog</h1>

      <form onSubmit={handleSearch} style={{ display: 'flex', gap: '0.75rem', marginBottom: '2rem', alignItems: 'flex-end' }}>
        <div className="form-group" style={{ flex: 1, marginBottom: 0 }}>
          <label htmlFor="book-search-input">Search</label>
          <input
            id="book-search-input"
            type="text"
            value={query}
            onChange={function (e) { setQuery(e.target.value); }}
            placeholder="Title or author name"
          />
        </div>

        <div className="form-group" style={{ width: '200px', marginBottom: 0 }}>
          <label htmlFor="genre-select">Genre</label>
          <select
            id="genre-select"
            value={selectedGenre}
            onChange={function (e) { setSelectedGenre(e.target.value); }}
          >
            <option value="">All genres</option>
            {GENRES.map(function (g) {
              return <option key={g} value={g}>{g}</option>;
            })}
          </select>
        </div>

        <button type="submit" disabled={isSearching}>
          {isSearching ? 'Searching...' : 'Search'}
        </button>

        {isFiltered && (
          <button type="button" onClick={handleClear} style={{ backgroundColor: 'var(--color-text-muted)' }}>
            Clear
          </button>
        )}
      </form>

      {bookList!.length === 0 ? (
        <p className="state-empty">No books matched your search.</p>
      ) : (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Title</th>
                <th>Author</th>
                <th>Genre</th>
                <th>Copies Available</th>
              </tr>
            </thead>
            <tbody>
              {bookList!.map(function (book: Book) {
                return (
                  <tr key={book._id}>
                    <td>
                      <Link to={`/books/${book._id}`}>{book.title}</Link>
                    </td>
                    <td>{book.author_name}</td>
                    <td>{book.genre}</td>
                    <td className="mono">{book.copies_available}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default BookList;
