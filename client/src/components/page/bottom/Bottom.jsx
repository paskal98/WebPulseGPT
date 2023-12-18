import styles from './Bottom.module.css';

export default function Bottom(){

    return <footer className={styles.bottom}>
        <div className={styles.content}>

            <div className={styles.bottom__cop}>© 2024 TUKE, edu.</div>

            <div className={styles.bottom__authority}>Developed by <span className={styles.bottom__authority__author}>Vlad Moskalenko</span> and <span className={styles.bottom__authority__author}>Eugene Shlapak</span> </div>

            <div className={styles.bottom__status}>
                <div className={styles.bottom__status__text}>Status</div>
                <div className={styles.bottom__status__icon}></div>
            </div>

        </div>
    </footer>

}