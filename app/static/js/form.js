(()=>{
    const EducationBlock = document.querySelector(".edu-block").cloneNode(true);
    const EducationContainer = document.querySelector("#education-container");

    document.querySelector("#add-education-block").addEventListener("click", e => {
        EducationContainer.appendChild(EducationBlock.cloneNode(true))
    })

    const CertificateBlock = document.querySelector(".certificate-block").cloneNode(true);
    const CertificatesContainer = document.querySelector("#certificates-container");

    document.querySelector("#add-certificate-block").addEventListener("click", e => {
        CertificatesContainer.appendChild(CertificateBlock.cloneNode(true))
    })

    const AwardHonorBlock = document.querySelector(".award-honor-block").cloneNode(true);
    const AwardsHonorsContainer = document.querySelector("#awards-honors-container");

    document.querySelector("#add-award-honor-block").addEventListener("click", e => {
        AwardsHonorsContainer.appendChild(AwardHonorBlock.cloneNode(true))
    })

    const SkillBlock = document.querySelector(".skill-block").cloneNode(true);
    if(SkillBlock.querySelector(".skill-level-describer")){
        SkillBlock.querySelector(".skill-level-describer").textContent = "-1";
    }
    const SkillsContainer = document.querySelector("#skills-container");

    document.querySelector("#add-new-skill-block").addEventListener("click", e => {
        SkillsContainer.appendChild(SkillBlock.cloneNode(true))
    })

    const ProjectBlock = document.querySelector(".project-block").cloneNode(true);
    const ProjectSContainer = document.querySelector("#projects-container");

    document.querySelector("#add-new-project-block").addEventListener("click", e => {
        ProjectSContainer.appendChild(ProjectBlock.cloneNode(true));
    })


    const WorkExperienceBlock = document.querySelector(".work-experience-block").cloneNode(true);
    const WorkExperiencesContainer = document.querySelector("#work-experiences-container");

    document.querySelector("#add-work-experience-block").addEventListener("click", e => {
        WorkExperiencesContainer.appendChild(WorkExperienceBlock.cloneNode(true))
    })

    const cleanInputValues = (anElement) => {
        anElement.querySelectorAll("input").forEach(input => { input.value = "" })
        anElement.querySelectorAll("textarea").forEach(input => { input.value = "" })
        anElement.querySelectorAll("textarea").forEach(input => { input.textContent = "" })
        anElement.querySelectorAll("input[type='range']").forEach(input => { input.value = "-1" })
    }
    cleanInputValues(EducationBlock)
    cleanInputValues(CertificateBlock)
    cleanInputValues(AwardHonorBlock)
    cleanInputValues(SkillBlock)
    cleanInputValues(ProjectBlock)
    cleanInputValues(WorkExperienceBlock)
})()