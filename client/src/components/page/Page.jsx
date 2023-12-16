import {useState} from "react";
import Header from "../header/Header.jsx";
import HomePage from "../content/HomePage.jsx";
import SignInUpPage from "../content/sign-in-up/SignInUpPage.jsx";
import Bottom from "../bottom/Bottom.jsx";

const pages =['home','signInUp']
export default function Page(){
    const [page, setPage] = useState(pages[1]);


    return (
        <>
            <Header/>
                {page==='home' && <HomePage/>}
                {page==='signInUp' && <SignInUpPage/>}
            <Bottom/>
        </>
    )
}