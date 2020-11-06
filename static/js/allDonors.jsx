function Donor({ orgname, totalAmount }) {
    const [isOpen, setIsOpen] = React.useState(false);
    const [candidates, setCandidates] = React.useState({});
    React.useEffect(() => {
        if (!isOpen) {
            return;
        }
        fetch(`/api/donors/${orgname}`).
            then((response) => response.json()).
            then((donor) => {
                console.log("Got donor response", donor);
                setCandidates(donor.donor);
            })
    }, [isOpen, orgname]) // dependency list (if these change, the function gets called)  
    return (
        <ReactBootstrap.Card>
            <ReactBootstrap.Card.Header>
                <ReactBootstrap.Accordion.Toggle as={ReactBootstrap.Button} onClick={() => { setIsOpen(true) }} variant="link" eventKey={orgname}>
                    <h5>{`${orgname} gave $${totalAmount.toLocaleString()}`}</h5> <button type="button">Add Star</button>
                </ReactBootstrap.Accordion.Toggle>
            </ReactBootstrap.Card.Header>
            {candidates.candidates &&
                <ReactBootstrap.Accordion.Collapse eventKey={orgname}>
                    <ReactBootstrap.Card.Body>
                        <br></br><h5>{orgname} gave {candidates.totals.d_perc}% to Democrats and {candidates.totals.r_perc}% to Republicans.</h5><br></br>
                        <div>
                            <ReactBootstrap.Table striped bordered hover size="sm">
                                <thead>
                                    <tr>
                                        <td><strong>Amount</strong></td>
                                        <td><strong>Party-State</strong></td>
                                        <td><strong>Candidate</strong></td>
                                    </tr>
                                </thead>
                                <tbody>
                                {candidates.candidates.map(candidate => 
                                    <tr key={candidate.firstlast}>
                                        <td>${candidate.total.toLocaleString()}</td>
                                        <td>{candidate.party}-{candidate.state}</td>
                                        <td>{candidate.firstlast}</td>
                                    </tr>   
                            
                                )}
                                </tbody>
                            </ReactBootstrap.Table>
                        </div>
                    </ReactBootstrap.Card.Body>
                </ReactBootstrap.Accordion.Collapse>
            }
        </ReactBootstrap.Card>
    )
}


function Industry({ catcode, catname, openCatname, setOpenCatname }) {
    const [donors, setDonors] = React.useState({}); 
    const isOpen = catname==openCatname;
    React.useEffect(() => {
        if (!isOpen) {
            return;
        }
        fetch(`/api/industries/${catcode}`).
            then((response) => response.json()).
            then((industry) => {
                console.log("Got industry response", industry);
                setDonors(industry.industry);
            })
    }, [isOpen, catcode]) // dependency list (if these change, the function gets called)
    const sortedDonation = donors.total_donated ? Object.entries(donors.total_donated)
        .sort(([, amount1], [, amount2]) => amount2 - amount1)
        .reduce((r, [orgname, amount]) => ({ ...r, [orgname]: amount }), {}) : {};
    return (
        <ReactBootstrap.Card>
            <ReactBootstrap.Card.Header>
                <ReactBootstrap.Button 
                    onClick={() => setOpenCatname(catname) }
                    aria-controls={`collapse-${catcode}`}
                    aria-expanded={isOpen}
                    >
                        <h4>{catname}</h4>
                </ReactBootstrap.Button>
            </ReactBootstrap.Card.Header>
            {donors.organizations &&
                <ReactBootstrap.Collapse in={isOpen}> 
                    <ReactBootstrap.Card.Body>
                    {Object.keys(sortedDonation).map(organization => {
                        return (
                            <Donor key={organization} orgname={organization} totalAmount={sortedDonation[organization]}></Donor>
                        )
                    })}
                    </ReactBootstrap.Card.Body>
                </ReactBootstrap.Collapse>
            }
        </ReactBootstrap.Card>
    )
}


function AllIndustries({ searchResult }) {
    console.log("hi margaret search result is:", searchResult)
    const [industries, setIndustries] = React.useState([]);
    const [openCatname, setOpenCatname] = React.useState(null)
    React.useEffect(() => {
        fetch('/api/industries').
        then((response) => response.json()).
        then((industries) => setIndustries(industries.industries));
    }, [])
    if (industries.length === 0) return <div>Loading...</div>
    const content = []
    for (const industry of industries) {
        content.push(<Industry key={industry.catcode} catcode={industry.catcode} catname={industry.catname} openCatname={openCatname} setOpenCatname={setOpenCatname} />);
    }
    return <ReactBootstrap.Accordion>{content}</ReactBootstrap.Accordion>
}


function Candidate({ firstlast, state, party }) {
    const [isOpen, setIsOpen] = React.useState(false);
    const [orgs, setOrgs] = React.useState({});
    React.useEffect(() => {
        if (!isOpen) {
            return;
        }
        fetch(`/api/candidates/${firstlast}`).
            then((response) => response.json()).
            then((candidate) => {
                console.log("Got candidate response", candidate);
                setOrgs(candidate.candidate);
            })
    }, [isOpen, firstlast])
    return (
        <ReactBootstrap.Card>
            <ReactBootstrap.Card.Header>
                <ReactBootstrap.Accordion.Toggle as={ReactBootstrap.Button} onClick={() => { setIsOpen(true) }} variant="link" eventKey={firstlast}>
                    <h5>{firstlast} ({party})</h5>
                </ReactBootstrap.Accordion.Toggle>
            </ReactBootstrap.Card.Header>
            {orgs.orgs &&
                <ReactBootstrap.Accordion.Collapse eventKey={firstlast}>
                    <ReactBootstrap.Card.Body>
                        <h5>{firstlast} received campaign contributions from:</h5>
                        <div>
                            <ReactBootstrap.Table striped bordered hover size="sm">
                                <thead>
                                    <tr>
                                        <td><strong>Company</strong></td>
                                        <td><strong>Amount</strong></td>
                                    </tr>
                                </thead>
                                <tbody>
                                {orgs.orgs.map(org => 
                                    <tr key={org.orgname}>
                                        <td>${org.amount.toLocaleString()}</td>
                                        <td>{org.orgname}</td>
                                    </tr>   
                                )}
                                </tbody>
                            </ReactBootstrap.Table>
                        </div>
                    </ReactBootstrap.Card.Body>
                </ReactBootstrap.Accordion.Collapse>
            }
        </ReactBootstrap.Card>
    )
}


function CandidateState({ firstlast, state, party, openState, setOpenState }) {

    const [candidates, setCandidates] = React.useState({});
    const isOpen = state == openState;
    React.useEffect(() => {
        if (!isOpen) {
            return;
        }
        fetch(`/api/states/${state}`).
            then((response) => response.json()).
            then((state) => {
                console.log("Got state response", state);
                setCandidates(state.state);
            })
    }, [isOpen, state])
    return (
        <ReactBootstrap.Card>
            <ReactBootstrap.Card.Header>
                <ReactBootstrap.Button
                    onClick={() => setIsOpen(!isOpen)}
                    onClick={() => setOpenState(state)}
                    aria-controls={`collapse-${state}`}
                    aria-expanded={isOpen}
                >
                    <h4>{state}</h4>
                </ReactBootstrap.Button>
            </ReactBootstrap.Card.Header>
            {candidates.candidates &&
                <ReactBootstrap.Collapse in={isOpen}>
                    <ReactBootstrap.Card.Body>
                        {candidates.candidates.map(candidate => {
                            return (
                                <Candidate key={candidate.firstlast} firstlast={candidate.firstlast} state={candidate.state} party={candidate.party}></Candidate>
                            )
                        })}
                    </ReactBootstrap.Card.Body>
                </ReactBootstrap.Collapse>
            }
        </ReactBootstrap.Card>
    )
}


function AllStates() {
    const [states, setStates] = React.useState([]);
    const [openState, setOpenState] = React.useState(null);
    React.useEffect(() => {
        fetch('/api/states').
            then((response) => response.json()).
            then((states) => setStates(states.states));
    }, [])
    if (states.length === 0) return <div>Loading...</div>
    const content = []
    for (const state of states) {
        content.push(<CandidateState key={state}
            state={state}
            openState={openState}
            setOpenState={setOpenState} />);
    }
    return <ReactBootstrap.Accordion>{content}</ReactBootstrap.Accordion>
}

function Home() {
    return(
        <h1>Welcome to Campaign Finance App</h1>
    )
}


function NavBar({ searchResult, setSearchResult }) {
    return (
        <div>
            <ReactBootstrap.Navbar bg="dark" variant="dark">
                <ReactBootstrap.Navbar.Brand href="#home">Campaign Finance App</ReactBootstrap.Navbar.Brand>
                <ReactBootstrap.Navbar.Toggle aria-controls="basic-navbar-nav" />
                <ReactBootstrap.Navbar.Collapse id="basic-navbar-nav">
                    <ReactBootstrap.Nav className="mr-auto">
                        <ReactRouterDOM.Link to="/home" className="nav-link" >Home</ReactRouterDOM.Link>
                        <ReactRouterDOM.Link to="/industries" className="nav-link" >Industries</ReactRouterDOM.Link>
                        <ReactRouterDOM.Link to="/candidates" className="nav-link" >Candidates</ReactRouterDOM.Link>
                    </ReactBootstrap.Nav>
                    <ReactBootstrap.Form inline>
                        <input value={searchResult} onChange={event => setSearchResult(event.target.value)} type="text" placeholder="Search" className="mr-sm-2" /> 
                        {/* <ReactBootstrap.FormControl type="text" placeholder="Search" className="mr-sm-2" /> */}
                        <ReactBootstrap.Button variant="outline-success">Search</ReactBootstrap.Button>
                    </ReactBootstrap.Form>
                </ReactBootstrap.Navbar.Collapse>
            </ReactBootstrap.Navbar>
        </div>
    )
}

function App() {
    const [searchResult, setSearchResult] = React.useState('')
    return (
        <ReactRouterDOM.BrowserRouter>
            <NavBar searchResult={searchResult} setSearchResult={setSearchResult} /> 
            <ReactRouterDOM.Switch>
                <ReactRouterDOM.Route path="/home" exact>
                    <Home />
                </ReactRouterDOM.Route>
                <ReactRouterDOM.Route path="/industries" exact>
                    <AllIndustries searchResult={searchResult} />
                </ReactRouterDOM.Route>
                <ReactRouterDOM.Route path="/candidates" exact>
                    <AllStates />
                </ReactRouterDOM.Route>
            </ReactRouterDOM.Switch>
        </ReactRouterDOM.BrowserRouter>
    );
}


ReactDOM.render(<App />, document.getElementById('root'))