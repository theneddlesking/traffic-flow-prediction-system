import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav className='main-nav'>
      <ul>
        <li>
          <Link to="/">Home</Link>
        </li>
        <li>
          <Link to="/map">Map</Link>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar