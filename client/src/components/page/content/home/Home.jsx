import styles from './Home.module.css'
import Button from "../../buttons/Button.jsx";
import Slider from "../../additional/slider-features/Slider.jsx";
import blob from "../../../../assets/blob.png";

export default function Home({onMenuChange}) {

    return <div className={styles.content}>

        <div className={styles.main}>

            <div className={styles.main__text}>
                <h1 className={styles.main__text__title}>
                    <span className={styles.main__text__title__ai}>AI </span>
                    Agent for
                    <span className={styles.main__text__title__defusion}> Innovative Dev.</span></h1>
                <h2 className={styles.main__text__descr}>Revolutionize web development with advanced GPT tech for streamlined application creation.</h2>
            </div>

            <div className={styles.main__features}>
                <Slider/>
                <Button onClickButton={onMenuChange} title={"Try It!"} spec_style={'try_it'}></Button>
            </div>

        </div>

        <div className={styles.blob}>
            <img src={blob} alt="blob"/>
        </div>

    </div>

}