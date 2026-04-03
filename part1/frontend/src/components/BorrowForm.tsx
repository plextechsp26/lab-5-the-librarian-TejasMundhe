import { useState } from 'react';
import { borrowBook } from '../api/library';

interface BorrowFormProps {
  bookId: string;
  /** Called after a successful borrow so the parent can re-fetch updated data. */
  onSuccess: () => void;
}

/** Form for borrowing a book. Calls onSuccess after a successful borrow so the parent can re-fetch. */
function BorrowForm({ bookId, onSuccess }: BorrowFormProps) {
  const [memberId, setMemberId] = useState<string>('');
  const [statusMessage, setStatusMessage] = useState<string | null>(null);
  const [isError, setIsError] = useState<boolean>(false);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!memberId.trim()) {
      setIsError(true);
      setStatusMessage('Please enter a Member ID.');
      return;
    }

    setIsSubmitting(true);
    setStatusMessage(null);

    try {
      await borrowBook(memberId.trim(), bookId);
      setIsError(false);
      setStatusMessage('Book borrowed successfully.');
      setMemberId('');
      onSuccess();
    } catch (err) {
      setIsError(true);
      setStatusMessage(err instanceof Error ? err.message : 'Could not complete the borrow request.');
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      {statusMessage && (
        <p className={`message ${isError ? 'message-error' : 'message-success'}`}>
          {statusMessage}
        </p>
      )}

      <div className="form-group">
        <label htmlFor="member-id-input">Member ID</label>
        <input
          id="member-id-input"
          type="text"
          value={memberId}
          onChange={function (e) { setMemberId(e.target.value); }}
          placeholder="Paste a member _id from the Members page"
          style={{ fontFamily: 'var(--font-mono)', fontSize: 'var(--text-sm)' }}
        />
      </div>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Processing...' : 'Borrow Book'}
      </button>
    </form>
  );
}

export default BorrowForm;
