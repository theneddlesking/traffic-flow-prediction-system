import './App.css'

function Home() {
  return (
    <>
        <div className="card">
          <h1>Traffic Flow Prediction System</h1>
          <hr />
          <p>
            This project implements a traffic flow prediction system, or TFPS for short.
            Accurate and timely traffic flow information is important for traffic authorities (such as VicRoads)
            to identify congested areas and implement traffic management policies to reduce congestion.
            <br /><br />
            It is also critical for route guidance systems (such as Google maps) to calculate the best
            routes for their users considering the traffic conditions potentially experienced along each route.
            Thanks to recent advancement in sensor technologies, traffic authorities are able to collect massive amount
            of traffic data to enable accurate predictions of traffic information (such as traffic flow, speed, travel time, etc.).
            <br /><br />
            The solution utilises historical traffic data for traffic flow prediction. The system will start as a basic
            system but then will become more advanced by adding further improvements and extensions.
          </p>
          <hr />
          <p>GitHub link: <a href='https://github.com/theneddlesking/traffic-flow-prediction-system' target='blank'>Traffic Flow Prediction System</a></p>
          <hr />
          <p>Group members:</p>
          <ul>
            <li>Olsen, Ned (104544609)</li>
            <li>Celestino, Josh (104550240)</li>
            <li>Chuchuva, Anton (104584362)</li>
          </ul>
        </div>
    </>
  )
}

export default Home
