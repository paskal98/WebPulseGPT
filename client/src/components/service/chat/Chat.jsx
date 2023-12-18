import styles from './Chat.module.css';
import ChatOption from "./ChatOption.jsx";
import ChatConversation from "./ChatConversation.jsx";
import {chatOptions} from "../data/chatOptions.js";
import {useEffect, useState} from "react";


export default function Chat({conversation,page, onOptionSelect,onConversationCreation}) {


    return <div className={styles.chat}>
        <ChatOption onOptionSelect={onOptionSelect}/>
        <ChatConversation conversation={conversation} onConversationCreation={onConversationCreation}
                          page={page}/>
    </div>

}