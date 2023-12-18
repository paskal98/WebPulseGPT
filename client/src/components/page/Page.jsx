import {useState} from "react";
import Header from "./header/Header.jsx";
import HomePage from "./content/home/HomePage.jsx";
import SignInUpPage from "./content/sign-in-up/SignInUpPage.jsx";
import Bottom from "./bottom/Bottom.jsx";
import {pages} from "./data/pages.js";

export default function Page({onMainChange}){
    const [page, setPage] = useState(pages[0]);

    function handleMenuChange(type){

        if(type==='try_it' || type==='form_log_in'){
           onMainChange('service');
           return;
        }

        if (type==='back'){
            type=pages[0];
        }
        setPage(type);
    }

    return (
        <>
            <Header onMenuChange={handleMenuChange} type={page}/>
                {page===pages[0] && <HomePage onMenuChange={handleMenuChange} />}
                {page===pages[1] && <SignInUpPage onMenuChange={handleMenuChange}/>}
            <Bottom/>
        </>
    )
}