import styles from './History.module.css';
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faEdit, faSearch} from "@fortawesome/free-solid-svg-icons";
import HistoryDate from "./HistoryDate.jsx";
import HistoryLabel from "./HistoryLabel.jsx";
import {Fragment} from "react";


const dataConversations = [

    {
        date: '17.12.2023',
        conversations: [
            {
                id: 5,
                name: "Chat 1"
            },
            {
                id: 4,
                name: "Chat 2"
            }
        ]
    },
    {
        date: '16.12.2023',
        conversations: [
            {
                id: 3,
                name: "Chat 3"
            },
            {
                id: 2,
                name: "Chat 4"
            },
            {
                id: 1,
                name: "Chat 5"
            }
        ]
    }

]


function getDateStatus(dateToCheck) {
    const today = new Date();
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    const lastWeek = new Date();
    lastWeek.setDate(lastWeek.getDate() - 7);

    today.setHours(0, 0, 0, 0);
    yesterday.setHours(0, 0, 0, 0);
    lastWeek.setHours(0, 0, 0, 0);
    dateToCheck.setHours(0, 0, 0, 0);


    if (dateToCheck.getTime() === today.getTime()) {
        return 'Today';
    } else if (dateToCheck.getTime() === yesterday.getTime()) {
        return 'Yesterday';
    } else if (dateToCheck >= lastWeek && dateToCheck < yesterday) {
        return 'Last 7 days';
    } else {
        return 'Older';
    }
}
const isYesterday = (dateToCheck) => {
    const today = new Date();

    return dateToCheck.getDate() === today.getDate() &&
        dateToCheck.getMonth() === today.getMonth() &&
        dateToCheck.getFullYear() === today.getFullYear();
};

export default function History({onChatSelected}) {

    return <div className={styles.conversation}>

        <div className={styles.conversation__options}>

            <div className={styles.conversation__options__item}>
                <FontAwesomeIcon icon={faSearch}/>
            </div>

            <div className={styles.conversation__options__item}>
                <FontAwesomeIcon icon={faEdit}/>
            </div>

        </div>


        <div className={styles.conversation__history}>



            {dataConversations.map((item, idx) => {

                let numbers = item.date.match(/\d+/g);
                let numberArray = numbers.map(num => parseInt(num));
                let dateToCheck = new Date(numberArray[2], numberArray[1] - 1, numberArray[0]);
                let date = getDateStatus(dateToCheck);

                return (
                    <Fragment key={idx}>
                        <HistoryDate title={date}/>
                        {item.conversations.map( conv => <HistoryLabel onChatSelected={onChatSelected} key={`${idx}-${conv.id}`} idConversation={conv.id} title={conv.name}/>)}
                    </Fragment>
                );

            })}


        </div>

    </div>

}