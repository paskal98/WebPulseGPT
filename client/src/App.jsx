import './App.css'
import Page from "./components/page/Page.jsx";
import {useState} from "react";
import Service from "./components/service/Service.jsx";

const routs =['page','service']
function App() {

    const [route, setRoute] = useState(routs[1]);

    function handleMainChange(type){
        setRoute(type);
    }


    return (
        <>

            {route===routs[0] && <Page onMainChange={handleMainChange}/>}
            {route===routs[1] && <Service onMainChange={handleMainChange}/>}

        </>
    )
}

export default App
