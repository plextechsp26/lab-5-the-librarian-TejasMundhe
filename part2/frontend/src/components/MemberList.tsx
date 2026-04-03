import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { fetchAllMembers, Member } from '../api/library';

/** Table of every registered member. Calls GET /members on mount. */
function MemberList() {
  const [memberList, setMemberList] = useState<Member[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(function () {
    async function loadMembers() {
      try {
        const members = await fetchAllMembers();
        setMemberList(members);
      } catch {
        setError('Could not load members. Is the Flask server running?');
      }
    }

    loadMembers();
  }, []);

  if (memberList === null && error === null) {
    return (
      <div className="page">
        <p className="state-loading">Loading members...</p>
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

  return (
    <div className="page">
      <h1>Members</h1>

      {memberList!.length === 0 ? (
        <p className="state-empty">No members registered yet. Run the seed script.</p>
      ) : (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Card Number</th>
              </tr>
            </thead>
            <tbody>
              {memberList!.map(function (member: Member) {
                return (
                  <tr key={member._id}>
                    <td>
                      <Link to={`/members/${member._id}`}>{member.name}</Link>
                    </td>
                    <td>{member.email}</td>
                    <td className="mono">{member.card_number ?? '—'}</td>
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

export default MemberList;
