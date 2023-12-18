import Home from "./Home.jsx";
import styles from './Homepage.module.css'

export default function HomePage({onMenuChange}) {

    return <div className={styles.content}>
        <Home onMenuChange={onMenuChange}/>
    </div>

}