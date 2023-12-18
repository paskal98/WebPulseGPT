import LeftBar from "./leftbar/LeftBar.jsx";
import History from "./history/History.jsx";
import Chat from "./chat/Chat.jsx";
import {useState} from "react";
import {chatOptions} from "./data/chatOptions.js";
import {conversations} from "./data/conversations.jsx";
import PopUp from "./leftbar/PopUp.jsx";
import {popUps} from "./data/popUps.js";

const pages = ['Welcome', ...chatOptions];

const defaultChat =
    {
        id:0,
        chats: [
            {
                participant: {
                    name:'WebPulsGPT'
                },
                conversation:<>Please give name of your new project</>
            }
        ],
        files:[]
    }



function getConversationById(id) {
    return id===0 ? defaultChat : conversations.find(conversation => conversation.id === id);
}



export default function Service({onMainChange}){
    const [idConversation, setIdConversation] = useState(0);
    const [conversation, setConversation] = useState(getConversationById(idConversation));
    const [page, setPage] = useState(pages[0]);
    const [popUp, setPopUp] = useState(popUps[0])

    function handleChatSelected(idConversation) {
        setIdConversation(idConversation);
        setConversation(getConversationById(idConversation));
        setPage(pages[1]);
    }

    function handleOptionSelect(type) {
        setPage(type);
    }

    function handleConversationCreation() {
        setPage(pages[1]);
    }

    function handleBarSelect(type) {
        if (type===popUps[4]){
            onMainChange('page');
            return
        }
        setPopUp(type);
    }


    return <div className='service'>

        <LeftBar onBarSelect={handleBarSelect}/>
        <History onChatSelected={handleChatSelected}/>
        <Chat onOptionSelect={handleOptionSelect} onConversationCreation={handleConversationCreation} page={page} conversation={conversation}/>

        {popUp!==popUps[0] && <PopUp type={popUp} onBarSelect={handleBarSelect} />}


    </div>
}