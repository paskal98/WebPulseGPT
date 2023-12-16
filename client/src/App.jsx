import './App.css'
import Page from "./components/page/Page.jsx";
import {useState} from "react";
import Service from "./components/service/Service.jsx";

const routs =['service','page']
function App() {

    const [route, setRoute] = useState(routs[0]);

    return (
        <>
            {route==='page' && <Page/>}
            {route==='service' && <Service/>}

        </>
    )
}

export default App
