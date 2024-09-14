import {Hero,Footer,CostumeReviews,PopularProducts,
  Services,SpecialOffer,Subcribe,SuperQuality} from "./sections/Export"
import { Nav } from "./Components/Nav"
  /*return (
    <h1 className="text-3xl font-bold underline">
      Hello world!!!!
    </h1>
  )
}*/
 const App =()=> {
  return (
    <main className="relative">
        <Nav/>
      <section className="xl:padding-l wide:padding-r padding-b">
        <Hero/>
      </section>
      <section className="padding">
        <PopularProducts/>
      </section>
      <section className="padding">
        <SuperQuality/>
      </section>
      <section className="padding-x py-10">
        <Services/>
      </section>
      <section className="padding">
        <SpecialOffer/>
      </section>
      <section className=" bg-pale-blue padding">
        <CostumeReviews/> 
      </section>
      <section className="padding-x sm:py-32 py-16 w-full bg-purple-200">
        <Subcribe/>
      </section>
      <section className="padding bg-black text-white">
        <Footer/>
      </section>
    </main>
  )
 }
 export default  App