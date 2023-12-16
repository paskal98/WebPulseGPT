import styles from './ButtonSignWith.module.css'
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";

export default function ButtonSignWith({title, faIcon}){
    return <button className={styles.button} >
        <div className={styles.button__icon}>
            <FontAwesomeIcon icon={faIcon}/>
        </div>
        <div  className={styles.button__title}>
            Sign with {title}
        </div>
    </button>
}