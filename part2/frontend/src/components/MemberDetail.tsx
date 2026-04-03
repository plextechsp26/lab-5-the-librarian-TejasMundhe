import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { fetchMemberById, MemberDetail as MemberDetailType } from '../api/library';

/** Formats an ISO date string to "14 Mar 2021", or returns null. */
function formatDate(dateString: string | null): string | null {
  if (!dateString) return null;
  return new Date(dateString).toLocaleDateString('en-GB', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  });
}

/** Detail page for a single member — contact info, library card, and borrow history. */
function MemberDetail() {
  const { id } = useParams<{ id: string }>();

  const [selectedMember, setSelectedMember] = useState<MemberDetailType | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(function () {
    async function loadMember() {
      try {
        const member = await fetchMemberById(id!);
        setSelectedMember(member);
      } catch {
        setError('Could not load member details. Is the Flask server running?');
      }
    }

    loadMember();
  }, [id]);

  if (selectedMember === null && error === null) {
    return (
      <div className="page">
        <p className="state-loading">Loading member...</p>
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

  const member = selectedMember!;

  return (
    <div className="page">
      <Link to="/members" className="back-link">All Members</Link>

      <h1>{member.name}</h1>

      <p className="section-header">Member Details</p>
      <div className="detail-grid">
        <span className="detail-label">Email</span>
        <span className="detail-value">{member.email}</span>

        <span className="detail-label">Member Since</span>
        <span className="detail-value mono">{formatDate(member.joined)}</span>
      </div>

      <p className="section-header">Library Card</p>
      {member.card ? (
        <div className="detail-grid">
          <span className="detail-label">Card Number</span>
          <span className="detail-value mono">{member.card.card_number}</span>

          <span className="detail-label">Issued</span>
          <span className="detail-value mono">{formatDate(member.card.issued)}</span>

          <span className="detail-label">Expires</span>
          <span className="detail-value mono">{formatDate(member.card.expires)}</span>

          <span className="detail-label">Status</span>
          <span className="detail-value">{member.card.status}</span>
        </div>
      ) : (
        <p className="state-empty">No library card on file.</p>
      )}

      <p className="section-header">Borrow History</p>

      {member.borrowed_books.length === 0 ? (
        <p className="state-empty">This member has not borrowed any books.</p>
      ) : (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Title</th>
                <th>Borrowed</th>
                <th>Returned</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {member.borrowed_books.map(function (record) {
                return (
                  <tr key={record.borrow_id}>
                    <td>
                      <Link to={`/books/${record.book_id}`}>{record.title}</Link>
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
    </div>
  );
}

export default MemberDetail;
