import styles from './Welcome.module.css';

export default function Welcome({onConversationCreation}){

    return <div className={styles.welcome}>

        <div className={styles.welcome__text}>
            Create your unique project fast and stand-full
        </div>

        <button onClick={onConversationCreation} className={styles.welcome__button}>Start</button>


    </div>

}