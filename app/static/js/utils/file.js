function getFileExtension(file){
    return `.${file.name.split('.').pop()}`;
}

export default getFileExtension