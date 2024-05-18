export const showErrorBanner = (errorText) => {
    $('#errorBanner').removeClass('d-none');
    $('#errorBanner').text(`One of your requests has failed. Please reload the page. Error: ${errorText}`)
};