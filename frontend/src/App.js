import React from 'react';
import JobTable from "./JobTable";

class App extends React.Component {
    // add header of website, table and HOWTO cards
    render() {
        return (
            <div className="App">
                <nav className="navbar navbar-light bg-light p-3 shadow p-3 mb-5 bg-white justify-content-around">
                    <div className="navbar-brand">
                        <h1>QueryClient</h1>
                        <div className="align-self-baseline">0.9.0</div>
                    </div>
                    <img width="240" src="uke_logo_large.png" alt=""/>
                </nav>
                <div className="card text-center shadow p-3 mb-5 bg-white rounded mx-auto" style={{maxWidth: "100rem",width: "95%"}}>
                    <h3 className="card-header">Offene Druckjobs</h3>
                    <div className="card-body">
                        <JobTable />
                    </div>
                </div>
                <div className="card text-center shadow p-3 mb-5 bg-white rounded mx-auto" style={{maxWidth: "30rem", width: "90%"}}>
                    <h3 className="card-header">Repetier Drucker Frontend</h3>
                    <div className="card-body">
                        <button type="button" className="btn btn-dark"
                                onClick={(e) =>(window.open('http://192.168.2.100:3344/', '_blank'))}>Öffne Frontend</button>
                    </div>
                </div>
                <div className="card text-center shadow p-3 mb-5 bg-white rounded mx-auto" style={{maxWidth: "85rem", width: "90%"}}>
                    <h3 className="card-header">HOW TO</h3>
                    <div className="card-body">
                        <h4>Einfügen von Druckjobs über GET-Request an das REST-API</h4>
                        <h5>(zB. in MobaXTerm)</h5>
                        <code>curl -X POST -H &quot;Content-Type: application/json&quot; -d '&#123;
                            "dataString" : "Mustermann|Max|1990-12-25|0815|Station 1|MedPrint3D|Med 100 mg|1.5|2022-09-09 15:21"
                        &#125;' -i localhost:50602/incoming</code>
                        <button className="btn btn-dark" style={{margin: "5px"}} onClick={() =>{navigator.clipboard.writeText(
                            "curl -X POST -H \"Content-Type: application/json\" -d '{\"dataString\" : \"Mustermann|Max|1990-12-25|0815|Station 1|MedPrint3D|Med 100 mg|1.5|2022-09-09 15:21\"}' -i localhost:50602/incoming")}}>Kopieren</button>
                        <h4>Zugriff auf die Oberfläche im Browser unter</h4>
                            <code>localhost:50604</code>
                    </div>
                </div>
            </div>
        );
    }
}

export default App;
