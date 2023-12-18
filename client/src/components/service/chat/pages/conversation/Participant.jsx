import styles from "./Participant.module.css";

export default function Participant({chat}){



    return <div className={styles.participant}>

        <div className={styles.participant__label}>

            {chat.participant.name==="WebPulsGPT" &&  <div className={styles.participant__label__icon}>AI</div>}
            {chat.participant.name!=="WebPulsGPT" &&  <div className={`${styles.participant__label__icon_user} ${styles.participant__label__icon}`}>{chat.participant.name.substring(0, 2).toUpperCase()}</div>}


            <div className={styles.participant__label_name}>{chat.participant.name}</div>

        </div>

        <div className={styles.participant__text}>
            <div className={styles.participant__text__chat}>{chat.conversation}</div>
        </div>

    </div>

}