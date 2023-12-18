import styles from './Conversation.module.css';
import Participant from "./Participant.jsx";
import {conversations} from "../../../data/conversations.jsx";


export default function Conversation({conversation}) {

    return <div className={styles.conversation}>

        {conversation.chats.map((item, idx) => <Participant key={idx} chat={item}/>)}

    </div>

}