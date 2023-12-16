import styles from "./Item.module.css";

export default function Item({title, descr, colorIdx}){

    const colors = [
        "#E1AC44",
        "#5687CF",
        "#56CF95",
        "#8453D4"
    ]




    return <div className={styles.item}>
        <div className={styles.item__icon} style={{backgroundColor: colors[colorIdx-1]}}></div>
        <div className={styles.item__text}>
            <div className={styles.item__text__title}>{title}</div>
            <div className={styles.item__text__descr}>{descr}</div>
        </div>
    </div>
}