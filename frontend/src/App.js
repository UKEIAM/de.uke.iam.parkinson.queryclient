import React from 'react';
import JobTable from "./JobTable";

class App extends React.Component {
    // add header of website, HOWTO and TODOs cards
    render() {
        return (
            <div className="App">
                <nav className="navbar navbar-light bg-light p-3 shadow p-3 mb-5 bg-white justify-content-around">
                    <div className="navbar-brand">
                        <h1>QueryClient</h1>
                        <div className="align-self-baseline">0.5.0</div>
                    </div>
                    <img width="240" src="uke_logo_large.png" alt=""/>
                </nav>
                <div className="card text-center shadow p-3 mb-5 bg-white rounded mx-auto" style={{maxWidth: "100rem",width: "95%"}}>
                    <h3 className="card-header">Offene Druckjobs</h3>
                    <div className="card-body">
                        <JobTable />
                    </div>
                </div>
                <div className="card text-center shadow p-3 mb-5 bg-white rounded mx-auto" style={{maxWidth: "85rem", width: "90%"}}>
                    <h3 className="card-header">HOW TO</h3>
                    <div className="card-body">
                        <h4>SHH-Tunnel zum REST-API und Frontend aufbauen</h4>
                        <code>ssh &lt;username&gt;@docker -L 50602:localhost:50602 -J jumper@stargate.fordo.de:56023</code>
                        <button className="btn btn-dark" style={{margin: "5px"}} onClick={() =>{navigator.clipboard.writeText("ssh &lt;username&gt;@docker -L 50602:localhost:50602 -J jumper@stargate.fordo.de:56023")}}>Kopieren</button>
                        <h4>SHH-Tunnel zum Frontend aufbauen</h4>
                        <code>ssh &lt;username&gt;@docker -L 50604:localhost:50604 -J jumper@stargate.fordo.de:56023</code>
                        <button className="btn btn-dark" style={{margin: "5px"}} onClick={() =>{navigator.clipboard.writeText("ssh &lt;username&gt;@docker -L 50604:localhost:50604 -J jumper@stargate.fordo.de:56023")}}>Kopieren</button>
                        <h4>Einfügen von Druckjobs über GET-Request an das REST-API</h4>
                        <h5>(zB. in MobaXTerm)</h5>
                        <code>curl -X POST -H &quot;Content-Type: application/json&quot; -d '&#123;
                        "surname&quot; : &quot;Mustermann&quot;&sbquo;
                        &quot;givenName&quot;:&quot;Max&quot;&sbquo;
                        &quot;birthday&quot;:&quot;1990-12-24&quot;&sbquo;
                        &quot;logisticsID&quot;:122&sbquo;
                        &quot;medicationName&quot;:&quot;Ibuprofen&quot;&sbquo;
                        &quot;medicationDose&quot;:&quot;70/30&quot;&sbquo;
                        &quot;medicationUnit&quot;:&quot;mg&quot;&sbquo;
                        &quot;medicationTimestamp&quot;:&quot;2022-01-01 15:22:15&quot;&sbquo;
                        &quot;hospitalWard&quot;:&quot;Station 1&quot;
                        &#125;' -i localhost:50602/incoming</code>
                        <button className="btn btn-dark" style={{margin: "5px"}} onClick={() =>{navigator.clipboard.writeText("curl -X POST -H \"Content-Type: application/json\" -d '{\"surname\" : \"ImGlueck\", \"givenName\":\"Hans\", \"birthday\":\"1990-12-24\", \"logisticsID\":122, \"medicationName\":\"Ibuprofen\", \"medicationDose\":\"30/30\", \"medicationUnit\":\"t\", \"medicationTimestamp\":\"2022-01-01 15:22:15\", \"hospitalWard\":\"Station 1\"}' -i localhost:50602/incoming")}}>Kopieren</button>
                        <h4>Zugriff auf die Oberfläche im Browser unter</h4>
                            <code>localhost:50604</code>
                    </div>
                </div>
                <div className="card text-center shadow p-3 mb-5 bg-white rounded mx-auto" style={{maxWidth: "50rem", width: "90%"}}>
                    <h3 className="card-header">TODOs</h3>
                    <div className="card-body">
                        <ul className="list-group">
                            <li className="list-group-item">Output für 3D-Drucker</li>
                            <li className="list-group-item">Output für Etikettendrucker</li>
                            <li className="list-group-item">Ports auf Maschine anpassen</li>
                        </ul>
                    </div>
                </div>
            </div>
        );
    }
}

export default App;
