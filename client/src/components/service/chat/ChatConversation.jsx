import styles from './ChatConversation.module.css'
import Welcome from "./pages/welcome/Welcome.jsx";
import {Fragment, useEffect, useState} from "react";
import {chatOptions} from "../data/chatOptions.js";
import Conversation from "./pages/conversation/Conversation.jsx";
import UserInput from "./pages/conversation/UserInput.jsx";
import Code from "./pages/code/Code.jsx";

const pages = ['Welcome',...chatOptions]

export default function ChatConversation({page,conversation,onConversationCreation}){


    const chatConvStyle = page===pages[2] ? `${styles.chatconv}` : `${styles.chatconv} ${styles.chatconv__h100vh}`;



    return <div className={chatConvStyle}>

        {page===pages[0]  && <Welcome onConversationCreation={onConversationCreation}/>}
        {page===pages[1]  &&
            <Fragment>

                <Conversation conversation={conversation}/>
                <UserInput/>
                <div className={styles.chatconv__blur}></div>

            </Fragment>
        }
        {page===pages[2] && <Code conversation={conversation} />}


    </div>

}