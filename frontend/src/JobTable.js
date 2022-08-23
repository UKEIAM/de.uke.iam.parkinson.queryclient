import React from 'react';

class JobTable extends React.Component {
    // just for reloading if needed
    constructor() {
        super();
        this.state = {
            currentId : 0,
            apiData : []
        }

        this.sendJob = this.sendJob.bind(this)
        this.deleteJob = this.deleteJob.bind(this)
    }

    async getData() {
        let result = await fetch('http://localhost:50602/outgoing')
            .then(response => response.json())
            .then(data => {return data})
            .catch((err) => {
                console.log(err.message);
            });
        return (
            result
        )
    }

    async componentDidMount() {
        this.setState({apiData : await this.getData()})
    }

    getHeader() {
        return (
            <thead>
            <tr>
                <th scope="col">InterneID</th>
                <th scope="col">Nachname</th>
                <th scope="col">Vorname</th>
                <th scope="col">Geburtstag</th>
                <th scope="col">LogistikID</th>
                <th scope="col">Medikation</th>
                <th scope="col">Dosis</th>
                <th scope="col">Einheit</th>
                <th scope="col">Gabezeitpunkt</th>
                <th scope="col">Station</th>
                <th scope="col">Button</th>
            </tr>
            </thead>
        );
    }

    async sendJob() {
        await fetch('http://localhost:50602/outgoing', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: this.state.currentId })
        }).catch((err) => {
            console.log(err.message);
        })
        console.log("Job " + this.state.currentId + " processed")
        this.setState({apiData : await this.getData()}, this.forceUpdate())
        // await this.getData()
        // this.forceUpdate()
    }

    async deleteJob() {
        await fetch('http://localhost:50602/outgoing', {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: this.state.currentId })
        }).catch((err) => {
            console.log(err.message);
        })
        console.log("Job " + this.state.currentId + " deleted")
        this.setState({apiData : await this.getData()}, this.forceUpdate())
    }

    getPopup(popupId, text, func) {
        return (
            <div className="modal hide fade" id={popupId} tabIndex="-1" role="dialog"
                 aria-labelledby="exampleModalLabel" aria-hidden="true" style={{color:"black"}}>
                <div className="modal-dialog" role="dialog">
                    <div className="modal-content">
                        <div className="modal-header">
                            <h3 className="text-center">Änderung Status Druckjob ID {this.state.currentId}</h3>
                            <button type="button" className="btn-close" data-dismiss="modal" aria-label="Close">
                            </button>
                        </div>
                        <div className="modal-body">
                            {text}
                        </div>
                        <div className="modal-footer">
                            <button type="button" className="btn btn-primary"
                                    data-dismiss="modal" onClick={() => {func()}}>Okay</button>
                            <button type="button" className="btn btn-secondary"
                                    data-dismiss="modal">Abbrechen</button>
                        </div>

                    </div>
                </div>
            </div>
        );
    }

    getButton(job) {
        return (
            <div className="container">
                <div className="dropdown">
                    <button className="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton"
                            data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"
                            onClick={() => this.setState({currentId : job.id})}>
                        Aktion
                    </button>
                    <div className="dropdown-menu" aria-labelledby="dropdownMenuButton">
                        <button className="dropdown-item" href="#" data-toggle="modal"
                                data-target="#sendPopup">Abschicken</button>
                        <button className="dropdown-item" href="#" data-toggle="modal"
                                data-target="#delPopup">Entfernen</button>
                    </div>
                </div>
            </div>
        );
    }

    render() {
        return (
            <div className="jobs-container">
                {this.getPopup("sendPopup", "Möchten Sie den Job wirklich absenden?", this.sendJob)}
                {this.getPopup("delPopup", "Möchten Sie den Job wirklich dauerhaft entfernen?", this.deleteJob)}
                <div className="table-responsive">
                    <table className="table table-hover table-dark mx-auto">
                        {this.getHeader()}
                        <tbody>
                        {this.state.apiData.map(job => {
                            return (
                                <tr>
                                    <th scope="row">{job.id}</th>
                                    <td>{job.surname}</td>
                                    <td>{job.givenName}</td>
                                    <td>{job.birthday}</td>
                                    <td>{job.logisticsID}</td>
                                    <td>{job.medicationName}</td>
                                    <td>{job.medicationDose}</td>
                                    <td>{job.medicationUnit}</td>
                                    <td>{job.medicationTimeStamp}</td>
                                    <td>{job.hospitalWard}</td>
                                    <td>
                                        {this.getButton(job)}
                                    </td>
                                </tr>
                            );
                        })}
                        </tbody>
                    </table>
                </div>
            </div>
        );
    }
}

export default JobTable;