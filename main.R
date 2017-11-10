library(shiny)

# Define UI for data upload app ----
ui <- fluidPage(
    titlePanel("Online Liver Radiomics - alpha version"),
    sidebarLayout(
        sidebarPanel(
            # Input: Select a file ----
            fileInput("file1", "Choose Tumor CT File",
                      multiple = FALSE,
                      accept = c(".nii")),
            fileInput("file2", "Choose Mask CT File",
                      multiple = FALSE,
                      accept = c(".nii"))
        ),
        
        # Main panel for displaying outputs ----
        mainPanel(
            h3(textOutput("status")),
            tableOutput("contents")       
        )
    )
)

options(shiny.maxRequestSize=60*1024^2) 
# Define server logic to read selected file ----
server <- function(input, output) {
    output$status <- renderText({ 
        req(input$file1)
        req(input$file1)
        if (is.null(input$file1)) return()
        if (is.null(input$file2)) return()
        tumorfile=paste0("/home/jeff/niirepo/",format(Sys.time(), "%Y%b%d_%H%M%S_"),"TUMOR.nii")
        maskfile=paste0("/home/jeff/niirepo/",format(Sys.time(), "%Y%b%d_%H%M%S_"),"MASK.nii")
        file.copy(input$file1$datapath, tumorfile)
        file.copy(input$file2$datapath, maskfile)
        "You have uploaded the tumor file and the mask file."
    })
    output$contents <- renderTable({
        # input$file1 will be NULL initially. After the user selects
        # and uploads a file, head of that data file by default,
        # or all rows if selected, will be shown.
        
        
        NULL
        #df <- read.csv(input$file1$datapath,
        #               header = input$header,
        #               sep = input$sep,
        #               quote = input$quote)   
        #if(input$disp == "head") {
        #    return(head(df))
        #}
        #else {
        #    return(df)
        #}
    })
}
# Run the app ----
shinyApp(ui, server)