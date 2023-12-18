import styles from './UserInput.module.css'
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faArrowCircleUp} from "@fortawesome/free-solid-svg-icons";

export default function UserInput(){

    return <div className={styles.userinput}>

        <input className={styles.userinput__input} placeholder="Write answer..."/>

        <button className={styles.userinput__button}>
            <FontAwesomeIcon icon={faArrowCircleUp}/>
        </button>

    </div>

}