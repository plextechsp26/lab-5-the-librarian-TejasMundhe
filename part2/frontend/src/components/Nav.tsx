import { Link, useLocation } from 'react-router-dom';

/** Returns "active" when the current URL path begins with prefix, else "". */
function getLinkClass(currentPath: string, prefix: string): string {
  return currentPath.startsWith(prefix) ? 'active' : '';
}

/** Site-wide navigation bar. Highlights the active link based on the current URL. */
function Nav() {
  const location = useLocation();

  return (
    <nav>
      <div className="nav-inner">
        <Link to="/books" className="nav-brand">
          The Librarian
        </Link>
        <ul className="nav-links">
          <li>
            <Link to="/books" className={getLinkClass(location.pathname, '/books')}>
              Books
            </Link>
          </li>
          <li>
            <Link to="/members" className={getLinkClass(location.pathname, '/members')}>
              Members
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default Nav;
